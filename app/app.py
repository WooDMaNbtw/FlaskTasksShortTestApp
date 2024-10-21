from flask import Flask, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask import render_template
from app.config import session, Task

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route(rule='/tasks/', methods=['GET'])
def list_tasks():
    """
    :return:  list of all tasks in database
    """
    try:
        tasks = session.query(Task).all()
        return jsonify([task.to_representation() for task in tasks], 200)
    except SQLAlchemyError as ex:
        session.rollback()
        return jsonify({
            "status": "server_error",
            "detail": str(ex)
        }, 500)


@app.route(rule='/tasks/', methods=['POST'])
def create_task():
    """
    Creates new task
    :return: created task
    """
    data = request.get_json()
    if 'title' not in data:
        return jsonify({
            "status": "required_field_error",
            "detail": "title field is required"
        }, 400)

    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        completed=data.get('completed', False)
    )

    try:
        session.add(new_task)
        session.commit()
        return jsonify(new_task.to_representation(), 201)
    except SQLAlchemyError as ex:
        session.rollback()
        return jsonify({
            "status": "server_error",
            "detail": str(ex)
        }, 500)

@app.route('/tasks/<int:id>/', methods=['PUT'])
def update_task(id):
    """
    Updates defined by id task
    :param id:
    :return: updated task
    """
    task = session.query(Task).get(id)
    if not task:
        return jsonify({
            "status": "not_found",
            "detail": "Task does not exist"
        }, 404)

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)

    try:
        session.commit()
        return jsonify(task.to_representation(), 200)
    except SQLAlchemyError as ex:
        session.rollback()
        return jsonify({
            "status": "server_error",
            "detail": str(ex)
        }, 500)

@app.route('/tasks/<int:id>/', methods=['DElETE'])
def delete_task(id):
    """
        Deletes defined by id task
        :param id:
        :return: Null
        """
    task = session.query(Task).get(id)
    if not task:
        return jsonify({
            "status": "not_found",
            "detail": "Task does not exist"
        }, 404)

    try:
        session.delete(task)
        session.commit()
        return jsonify(None, 204)
    except SQLAlchemyError as ex:
        session.rollback()
        return jsonify({
            "status": "server_error",
            "detail": str(ex)
        }, 500)


if __name__ == '__main__':
    app.run(debug=True)