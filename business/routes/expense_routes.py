# routes/expense_routes.py
from flask import jsonify, request, render_template

def init_expense_routes(app, db):
    """Initialize expense routes"""
    
    @app.route('/expenses')
    def manage_expenses():
        """Expenses management page"""
        return render_template('expenses.html')

    @app.route('/api/expenses', methods=['GET'])
    def api_get_expenses():
        """Get all expenses with filtering"""
        try:
            category_filter = request.args.get('category')
            month_filter = request.args.get('month')
            
            if category_filter and month_filter:
                query = """
                    SELECT * FROM expenses 
                    WHERE category = %s AND DATE_FORMAT(expense_date, '%%Y-%%m') = %s
                    ORDER BY expense_date DESC, expense_id DESC
                """
                expenses = db.execute_query(query, (category_filter, month_filter), fetch=True)
            elif category_filter:
                query = "SELECT * FROM expenses WHERE category = %s ORDER BY expense_date DESC, expense_id DESC"
                expenses = db.execute_query(query, (category_filter,), fetch=True)
            elif month_filter:
                query = "SELECT * FROM expenses WHERE DATE_FORMAT(expense_date, '%%Y-%%m') = %s ORDER BY expense_date DESC, expense_id DESC"
                expenses = db.execute_query(query, (month_filter,), fetch=True)
            else:
                query = "SELECT * FROM expenses ORDER BY expense_date DESC, expense_id DESC"
                expenses = db.execute_query(query, fetch=True)
                
            return jsonify({'success': True, 'expenses': expenses})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/expenses', methods=['POST'])
    def api_add_expense():
        """Add new expense"""
        try:
            data = request.json
            query = """
                INSERT INTO expenses (expense_date, category, description, amount, payment_method, receipt_info)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            db.execute_query(query, (
                data['expense_date'],
                data['category'],
                data['description'],
                data['amount'],
                data['payment_method'],
                data.get('receipt_info', '')
            ))
            return jsonify({'success': True, 'message': 'Expense recorded successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/expenses/<int:expense_id>', methods=['GET'])
    def api_get_expense(expense_id):
        """Get single expense"""
        try:
            expense = db.execute_query(
                "SELECT * FROM expenses WHERE expense_id = %s", 
                (expense_id,), 
                fetch=True
            )
            if expense:
                return jsonify({'success': True, 'expense': expense[0]})
            else:
                return jsonify({'success': False, 'message': 'Expense not found'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
    def api_update_expense(expense_id):
        """Update expense"""
        try:
            data = request.json
            query = """
                UPDATE expenses 
                SET expense_date = %s, category = %s, description = %s, amount = %s, 
                    payment_method = %s, receipt_info = %s
                WHERE expense_id = %s
            """
            db.execute_query(query, (
                data['expense_date'],
                data['category'],
                data['description'],
                data['amount'],
                data['payment_method'],
                data.get('receipt_info', ''),
                expense_id
            ))
            return jsonify({'success': True, 'message': 'Expense updated successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
    def api_delete_expense(expense_id):
        """Delete expense"""
        try:
            db.execute_query("DELETE FROM expenses WHERE expense_id = %s", (expense_id,))
            return jsonify({'success': True, 'message': 'Expense deleted successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/expenses_stats')
    def api_expenses_stats():
        """Get expenses statistics"""
        try:
            total_expenses = db.execute_query("SELECT SUM(amount) as total FROM expenses", fetch=True)[0]['total'] or 0
            total_transactions = db.execute_query("SELECT COUNT(*) as count FROM expenses", fetch=True)[0]['count']
            
            # This month expenses
            this_month_expenses = db.execute_query("""
                SELECT SUM(amount) as total FROM expenses 
                WHERE DATE_FORMAT(expense_date, '%%Y-%%m') = DATE_FORMAT(CURDATE(), '%%Y-%%m')
            """, fetch=True)[0]['total'] or 0
            
            # Number of categories
            expense_categories = db.execute_query("SELECT COUNT(DISTINCT category) as count FROM expenses", fetch=True)[0]['count']
            
            # Largest category
            largest_category = db.execute_query("""
                SELECT category, SUM(amount) as total 
                FROM expenses 
                GROUP BY category 
                ORDER BY total DESC 
                LIMIT 1
            """, fetch=True)
            largest_category_name = largest_category[0]['category'] if largest_category else 'N/A'
            
            return jsonify({
                'success': True,
                'total_expenses': float(total_expenses),
                'this_month_expenses': float(this_month_expenses),
                'total_transactions': total_transactions,
                'expense_categories': expense_categories,
                'largest_category': largest_category_name
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/monthly_expenses')
    def api_monthly_expenses():
        """Get current month expenses by category"""
        try:
            categories = db.execute_query("""
                SELECT category, SUM(amount) as amount 
                FROM expenses 
                WHERE DATE_FORMAT(expense_date, '%%Y-%%m') = DATE_FORMAT(CURDATE(), '%%Y-%%m')
                GROUP BY category 
                ORDER BY amount DESC
            """, fetch=True)
            
            total_monthly = sum(cat['amount'] for cat in categories) if categories else 0
            
            return jsonify({
                'success': True,
                'categories': categories or [],
                'total_monthly': float(total_monthly)
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/profit_calculation')
    def api_profit_calculation():
        """Calculate profit (revenue - expenses)"""
        try:
            total_revenue = db.execute_query("SELECT SUM(total_amount) as total FROM sales", fetch=True)[0]['total'] or 0
            total_expenses = db.execute_query("SELECT SUM(amount) as total FROM expenses", fetch=True)[0]['total'] or 0
            
            return jsonify({
                'success': True,
                'total_revenue': float(total_revenue),
                'total_expenses': float(total_expenses)
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})