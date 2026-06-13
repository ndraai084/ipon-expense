from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, make_response
from services.auth_service import register_user, login_user
from services.services import (
    get_transactions, add_transaction, edit_transaction, delete_transaction,
    calculate_balance, calculate_total_income, calculate_total_expense,
    compute_spending_by_category,
    get_category_chart_data, get_income_expense_chart_data, get_monthly_chart_data,
    get_categories, add_category, delete_category,
    get_budget, set_budget, calculate_current_month_expense
)
import pandas as pd  # sir paul library ng python

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.template_filter('currency')
def currency(value):

    try:

        return "{:,.2f}".format(
            float(value)
        )

    except:

        return "0.00"

@app.context_processor
def inject_nav_categories():
    # Categories for the global mobile "add transaction" bottom sheet,
    # which appears on every page (not just the ones that pass categories).
    if 'user' in session:
        try:
            return {'nav_categories': get_categories(session['user']['uid'])}
        except Exception:
            return {'nav_categories': []}
    return {'nav_categories': []}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/sw.js')
def service_worker():
    # Served from the root so the worker's scope covers the whole site
    # (a worker under /static/ could only control /static/*).
    response = make_response(
        send_from_directory('static', 'sw.js')
    )
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response

@app.route('/offline')
def offline():
    return render_template('offline.html')

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        identifier = request.form['identifier']
        password = request.form['password']

        user = login_user(
            identifier,
            password
        )

        if user:
            session['user'] = user
            return redirect(
                url_for('dashboard')
            )

        return render_template(
            'login.html',
            error='Invalid credentials'
        )

    return render_template(
        'login.html'
    )

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = register_user(
            username,
            email,
            password
        )

        if user:
            return redirect(
                url_for('login')
            )

        return render_template(
            'register.html',
            error='Registration failed'
        )

    return render_template(
        'register.html'
    )

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    print(session['user'])
    transactions = get_transactions(user['uid'])

    recent_transactions = transactions[:10]
    balance = total_income = total_expense = 0
    category_totals = {}
    month_expense = 0
    budget = get_budget(user['uid'])

    category_chart = {
        "labels": [],
        "data": []
    }

    income_expense_chart = {
        "labels": ["Income", "Expense"],
        "data": [0, 0]
    }

    monthly_chart = {
        "labels": [],
        "income": [],
        "expense": []
    }

    if transactions:
        df = pd.DataFrame(transactions)
        balance = calculate_balance(df)
        total_income = calculate_total_income(df)
        total_expense = calculate_total_expense(df)
        category_totals = compute_spending_by_category(df)
        category_chart = get_category_chart_data(df)
        income_expense_chart = get_income_expense_chart_data(df)
        monthly_chart = get_monthly_chart_data(df)
        month_expense = calculate_current_month_expense(df)

    return render_template('dashboard.html',
        user=user,
        transactions=recent_transactions,
        balance=balance,
        total_income=total_income,
        total_expense=total_expense,
        category_totals=category_totals,
        category_chart_data=category_chart,
        income_expense_chart_data=income_expense_chart,
        monthly_chart_data=monthly_chart,
        categories=get_categories(user['uid']),
        budget=budget,
        month_expense=month_expense
    )

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    error = None
    success = None

    transactions = get_transactions(
        user['uid']
    )

    transaction_count = len(
        transactions
    )

    income_count = len([
        t for t in transactions
        if t.get('type') == 'income'
    ])

    expense_count = len([
        t for t in transactions
        if t.get('type') == 'expense'
    ])

    if request.method == 'POST':
        old_pass = request.form.get('old_password')
        new_pass = request.form.get('new_password')
        confirm_pass = request.form.get('confirm_password')

        if new_pass != confirm_pass:
            error = "New passwords do not match."
        else:
            # Use Firebase REST API or Firestore hashed password
            # Example for Firebase REST login verification
            from services.auth_service import login_user
            check = login_user(user['email'], old_pass)
            if check:
                # Update password via Firebase Admin SDK or Firestore
                from firebase_admin import auth
                auth.update_user(user['uid'], password=new_pass)
                success = "Password updated successfully."
            else:
                error = "Old password is incorrect."

    return render_template(
        'settings.html',

        user=user,

        error=error,

        success=success,

        transaction_count=
            transaction_count,

        income_count=
            income_count,

        expense_count=
            expense_count,

        categories=
            get_categories(user['uid']),

        budget=
            get_budget(user['uid'])
    )

@app.route('/budget', methods=['POST'])
def update_budget():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']

    set_budget(
        user['uid'],
        request.form.get('budget', 0)
    )

    return redirect(url_for('settings'))

@app.route('/categories/add', methods=['POST'])
def add_cat():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']

    add_category(
        user['uid'],
        request.form.get('category_name', '')
    )

    return redirect(url_for('settings'))

@app.route('/categories/delete', methods=['POST'])
def delete_cat():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']

    delete_category(
        user['uid'],
        request.form.get('category_name', '')
    )

    return redirect(url_for('settings'))

@app.route('/transactions/add', methods=['POST'])
def add_trans():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    from datetime import datetime

    date_value = request.form.get('date')
    time_value = request.form.get('time')

    transaction_datetime = datetime.now()

    if date_value:

        if time_value:

            transaction_datetime = datetime.strptime(
                f"{date_value} {time_value}",
                "%Y-%m-%d %H:%M"
            )

        else:

            transaction_datetime = datetime.strptime(
                date_value,
                "%Y-%m-%d"
            )

    transaction_type = request.form['type']

    category = request.form.get(
        'category',
        ''
    )

    if transaction_type == 'income':
        category = ''

    data = {
        'amount': float(request.form['amount']),
        'type': transaction_type,
        'category': category,
        'note': request.form['note'],
        'date': transaction_datetime
    }
    add_transaction(user['uid'], data)
    return redirect(url_for('dashboard'))

@app.route('/transactions/edit/<trans_id>', methods=['POST'])
def edit_trans(trans_id):

    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']

    from datetime import datetime

    date_value = request.form.get('date')
    time_value = request.form.get('time')

    transaction_datetime = datetime.now()

    if date_value:

        if time_value:

            transaction_datetime = datetime.strptime(
                f"{date_value} {time_value}",
                "%Y-%m-%d %H:%M"
            )

        else:

            transaction_datetime = datetime.strptime(
                date_value,
                "%Y-%m-%d"
            )

    transaction_type = request.form['type']

    category = request.form.get(
        'category',
        ''
    )

    if transaction_type == 'income':
        category = ''

    updated_data = {
        'amount': float(request.form['amount']),
        'type': transaction_type,
        'category': category,
        'note': request.form['note'],
        'date': transaction_datetime
    }

    edit_transaction(
        user['uid'],
        trans_id,
        updated_data
    )

    return redirect(
        url_for('transactions')
    )

@app.route('/transactions/delete/<trans_id>')
def delete_trans(trans_id):

    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']

    delete_transaction(
        user['uid'],
        trans_id
    )

    return redirect(
        url_for('transactions')
    )


@app.route('/analytics')
def analytics():

    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']

    transactions = get_transactions(
        user['uid']
    )

    category_chart = {
        "labels": [],
        "data": []
    }

    income_expense_chart = {
        "labels": ["Income", "Expense"],
        "data": [0, 0]
    }

    monthly_chart = {
        "labels": [],
        "income": [],
        "expense": []
    }

    balance = 0
    total_income = 0
    total_expense = 0

    if transactions:

        df = pd.DataFrame(
            transactions
        )

        balance = calculate_balance(df)

        total_income = calculate_total_income(df)

        total_expense = calculate_total_expense(df)

        category_chart = get_category_chart_data(df)

        income_expense_chart = get_income_expense_chart_data(df)

        monthly_chart = get_monthly_chart_data(df)

    return render_template(
        'analytics.html',

        user=user,

        balance=balance,

        total_income=total_income,

        total_expense=total_expense,

        category_chart_data=category_chart,

        income_expense_chart_data=
            income_expense_chart,

        monthly_chart_data=
            monthly_chart
    )

@app.route('/transactions')
def transactions():

    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']

    transactions = get_transactions(
        user['uid']
    )

    return render_template(
        'transactions.html',
        transactions=transactions,
        categories=get_categories(user['uid'])
    )

if __name__=="__main__":
    app.run(debug=True)