from app import app, db
from models import Task, CATEGORIES, PRIORITY_ORDER
from flask import flash, jsonify, redirect, render_template, request, url_for
from datetime import datetime
from sqlalchemy import case


def _parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None


def _get_filtered_tasks():
    filter_type = request.args.get('filter', 'all')
    category = request.args.get('category', 'all')
    search = request.args.get('q', '').strip()
    sort = request.args.get('sort', 'created_desc')

    query = Task.query

    if filter_type == 'active':
        query = query.filter_by(done=False)
    elif filter_type == 'completed':
        query = query.filter_by(done=True)

    if category != 'all':
        query = query.filter_by(category=category)

    if search:
        like = f'%{search}%'
        query = query.filter(db.or_(Task.content.ilike(like), Task.notes.ilike(like)))

    if sort == 'due_date':
        query = query.order_by(Task.due_date.is_(None), Task.due_date.asc())
    elif sort == 'priority':
        priority_case = case(
            (Task.priority == 'high', 0),
            (Task.priority == 'medium', 1),
            else_=2,
        )
        query = query.order_by(priority_case, Task.created_at.desc())
    elif sort == 'created_asc':
        query = query.order_by(Task.created_at.asc())
    else:
        query = query.order_by(Task.created_at.desc())

    return query.all()


def _task_stats():
    all_tasks = Task.query.all()
    total = len(all_tasks)
    completed = sum(1 for t in all_tasks if t.done)
    active = total - completed
    overdue = sum(1 for t in all_tasks if t.is_overdue)
    due_today = sum(1 for t in all_tasks if t.is_due_today and not t.done)
    return {
        'total': total,
        'completed': completed,
        'active': active,
        'overdue': overdue,
        'due_today': due_today,
    }


@app.route('/')
@app.route('/index')
def tasks_list():
    tasks = _get_filtered_tasks()
    stats = _task_stats()
    return render_template(
        'index.html',
        tasks=tasks,
        filter=request.args.get('filter', 'all'),
        category=request.args.get('category', 'all'),
        search=request.args.get('q', ''),
        sort=request.args.get('sort', 'created_desc'),
        categories=CATEGORIES,
        stats=stats,
    )


@app.route('/task', methods=['POST'])
def add_task():
    content = request.form.get('content', '').strip()
    priority = request.form.get('priority', 'medium')
    category = request.form.get('category', 'general')
    due_date_str = request.form.get('due_date')
    notes = request.form.get('notes', '').strip() or None

    if not content:
        flash('Please enter a task title.', 'warning')
        return redirect(request.referrer or url_for('tasks_list'))

    due_date = _parse_date(due_date_str)
    if due_date_str and due_date is None:
        flash('Invalid date format. Use YYYY-MM-DD.', 'warning')
        return redirect(request.referrer or url_for('tasks_list'))

    task = Task(content, priority=priority, due_date=due_date, category=category, notes=notes)
    db.session.add(task)
    db.session.commit()
    flash('Task added successfully.', 'success')
    return redirect(request.referrer or url_for('tasks_list'))


@app.route('/toggle', methods=['POST'])
def toggle_status():
    task_id = request.form.get('task_id')
    if not task_id:
        return {'error': 'Task ID required'}, 400
    task = db.session.get(Task, task_id)
    if not task:
        return {'error': 'Task not found'}, 404
    task.done = not task.done
    task.updated_at = datetime.utcnow()
    db.session.commit()
    stats = _task_stats()
    return jsonify({
        'id': task.id,
        'done': task.done,
        'active_count': stats['active'],
        'completed_count': stats['completed'],
    })


@app.route('/edit', methods=['POST'])
def edit_task():
    task_id = request.form.get('task_id')
    edit_text = request.form.get('edit_text', '').strip()
    priority = request.form.get('priority', 'medium')
    category = request.form.get('category', 'general')
    due_date_str = request.form.get('due_date')
    notes = request.form.get('notes', '').strip() or None

    if not edit_text:
        flash('Please enter text for your task.', 'warning')
        return redirect(request.referrer or url_for('tasks_list'))

    task = db.session.get(Task, task_id)
    if not task:
        flash('Task not found.', 'danger')
        return redirect(url_for('tasks_list'))

    due_date = _parse_date(due_date_str)
    if due_date_str and due_date is None:
        flash('Invalid date format. Use YYYY-MM-DD.', 'warning')
        return redirect(request.referrer or url_for('tasks_list'))

    task.content = edit_text
    task.priority = priority
    task.category = category
    task.due_date = due_date
    task.notes = notes
    task.updated_at = datetime.utcnow()
    db.session.commit()
    flash('Task updated.', 'success')
    return redirect(request.referrer or url_for('tasks_list'))


@app.route('/delete', methods=['POST'])
def delete_task():
    task_id = request.form.get('task_id')
    if not task_id:
        flash('Task ID required.', 'warning')
        return redirect(url_for('tasks_list'))
    task = db.session.get(Task, task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted.', 'success')
    else:
        flash('Task not found.', 'danger')
    return redirect(request.referrer or url_for('tasks_list'))


@app.route('/finished', methods=['POST'])
def resolve_tasks():
    active_tasks = Task.query.filter_by(done=False).all()
    for task in active_tasks:
        task.done = True
        task.updated_at = datetime.utcnow()
    db.session.commit()
    flash('All tasks marked as completed.', 'success')
    return redirect(url_for('tasks_list'))


@app.route('/clear-completed', methods=['POST'])
def clear_completed():
    completed = Task.query.filter_by(done=True).all()
    count = len(completed)
    for task in completed:
        db.session.delete(task)
    db.session.commit()
    flash(f'Removed {count} completed task{"s" if count != 1 else ""}.', 'success')
    return redirect(request.referrer or url_for('tasks_list'))
