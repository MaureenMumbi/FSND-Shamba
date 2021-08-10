import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from database.models import setup_db, Procedure, Worker, Fields, Inputs
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to a farming tracker API system'
    })


@app.route('/procedures', methods=['GET'])
@requires_auth('get:procedures')
def get_procedures(payload):
        procedures = Procedure.query.all()
        if not procedures:
            abort(404)

        formattedprocedure = [procedure.format() for procedure in procedures]
        for procedure in formattedprocedure:
            workername = get_worker(procedure['worker'])
            fieldname = get_field(procedure['field'])
            inputname = get_input(procedure['input'])
            procedure['worker'] = workername
            procedure['field'] = fieldname
            procedure['input'] = inputname

        return jsonify({
            'success': True,
            'total_procedures': len(procedures),
            'procedures': formattedprocedure
        }), 200


def get_worker(workerid):
        worker = Worker.query.filter_by(id=workerid).first().name
        return worker


def get_input(inputid):
        input = Inputs.query.filter_by(id=inputid).first().name
        return input


def get_field(fieldid):
       field = Fields.query.filter_by(id=fieldid).first().name
       return field

    # add procedures


@app.route('/procedures', methods=['POST'])
@requires_auth('post:procedures')
def createprocedure(payload):
        data = request.get_json()

        if not data:
            abort(404)

        try:
            new_name = data.get('name', None)
            new_date = data.get('date', None)
            new_activity = data.get('activity', None)
            new_field_id = data.get('field_id', None)
            new_worker_id = data.get('worker_id', None)
            new_input_id = data.get('input_id', None)
            new_inputs_qty = data.get('inputs_quantity', None)
            new_image_link = data.get('image_link', None)
            procedure = Procedure(name=new_name,
                                  date=new_date,
                                  activity=new_activity,
                                  field_id=new_field_id,
                                  worker_id=new_worker_id,
                                  input_id=new_input_id,
                                  inputs_quantity=new_inputs_qty,
                                  image_link=new_image_link)
            procedure.insert()
        except Exception as e:
            abort(500)

        return jsonify({
            'success': True,
            'procedure': procedure.format(),
            'created': procedure.id
        })

    #  Update Procedure
@app.route('/procedures/<int:id>', methods=['PATCH'])
@requires_auth('patch:procedures')
def update_procedure(payload, id):
        data = request.get_json()
        procedure = Procedure.query.filter(Procedure.id == id).one_or_none()

        if not procedure:
            abort(404)

        try:
            updated_name = data.get('name', None)
            updated_date = data.get('date', None)
            updated_activity = data.get('activity', None)
            updated_field = data.get('field_id', None)
            updated_worker = data.get('worker_id', None)
            updated_input = data.get('input_id', None)
            updated_inputs_quantity = data.get('inputs_quantity', None)
            updated_image_link = data.get('image_link', None)

            if updated_name:
                procedure.name = updated_name
            if updated_date:
                procedure.date = updated_date
            if updated_activity:
                procedure.activity = updated_activity
            if updated_field:
                procedure.field = updated_field
            if updated_worker:
                procedure.worker_id = updated_worker
            if updated_input:
                procedure.input_id = updated_input
            if updated_inputs_quantity:
                procedure.inputs_quantity = updated_inputs_quantity
            if updated_image_link:
                procedure.image_link = updated_image_link

            procedure.update()

        except BaseException:
            abort(400)

        return jsonify({
            'success': True,
            'procedure': [procedure.format()]
        }), 200

    # Delete Procedure


@app.route('/procedures/<id>', methods=['DELETE'])
@requires_auth('delete:procedures')
def delete_procedure(payload, id):
        procedure = Procedure.query.filter(Procedure.id == id).one_or_none()

        if not procedure:
            abort(404)
        try:
            procedure.delete()
        except BaseException:
            abort(400)

        return jsonify({
            'success': True,
            'delete': id
        }), 200

    # get workers


@app.route('/workers', methods=['GET'])
@requires_auth('get:workers')
def get_workers(payload):
        workers = Worker.query.all()
        if not workers:
            abort(404)
        return jsonify({
            'success': True,
            'workers': [worker.format() for worker in workers]
        }), 200

    # Add workers
@app.route('/workers', methods=['POST'])
@requires_auth('post:workers')
def create_workers(payload):
        data = request.get_json()
        try:
            new_name = data.get('name', None)
            new_national_id = data.get('national_id', None)
            new_phone_number = data.get('phone_number', None)
            new_type = data.get('type', None)

            worker = Worker(name=new_name,
                            national_id=new_national_id,
                            phone_number=new_phone_number,
                            type=new_type,
                            )
            worker.insert()
        except Exception as e:
            print(e)
            abort(404)

        return jsonify({
            'success': True,
            'worker': worker.format()
        })

    # Delete Worker


@app.route('/workers/<id>', methods=['DELETE'])
@requires_auth('delete:workers')
def delete_worker(payload, id):
        worker = Worker.query.filter(Worker.id == id).one_or_none()

        if not worker:
            abort(404)
        try:
            worker.delete()
        except BaseException:
            abort(400)

        return jsonify({
            'success': True,
            'delete': id
        }), 200

    #  Update Worker


@app.route('/workers/<int:id>', methods=['PATCH'])
@requires_auth('patch:workers')
def update_workers(payload, id):
        data = request.get_json()
       
        worker = Worker.query.filter(Worker.id == id).one_or_none()

        if not worker:
            abort(404)

        try:
            updated_name = data.get('name', None)
            updated_id = data.get('national_id', None)
            updated_no = data.get('phone_number', None)
            updated_type = data.get('type', None)

            if updated_name:
                worker.name = updated_name
            if updated_id:
                worker.national_id = updated_id
            if updated_no:
                worker.phone_number = updated_no
            if updated_type:
                worker.type = updated_type

            worker.update()

        except BaseException as e:
            print(f'Error ==> {e}')
            abort(400)

        return jsonify({
            'success': True,
            'worker': [worker.format()]
        }), 200

    # Get Inputs

@app.route('/inputs', methods=['GET'])
@requires_auth('get:inputs')
def get_inputs(payload):
        inputs = Inputs.query.all()
        if not inputs:
            abort(404)

        return jsonify({
            'success': True,
            'inputs': [input.format() for input in inputs]
        }), 200


    # Add Inputs
@app.route('/inputs', methods=['POST'])
@requires_auth('post:inputs')
def create_inputs(payload):
        data = request.get_json()
      
        try:
            new_name = data.get('name', None)
            new_quantity = data.get('quantity', None)
            new_type = data.get('type', None)
            new_metrics = data.get('metrics', None)

            inputs = Inputs(name=new_name,
                            quantity=new_quantity,
                            type=new_type,
                            metrics= new_metrics
                            )
            inputs.insert()
        except Exception as e:
            print(e)
            abort(404)

        return jsonify({
            'success': True,
            'inputs': inputs.format()
        })
    # Delete Inputs


@app.route('/inputs/<id>', methods=['DELETE'])
@requires_auth('delete:inputs')
def delete_inputs(payload, id):
        input = Inputs.query.filter(Inputs.id == id).one_or_none()

        if not input:
            abort(404)
        try:
            input.delete()
        except BaseException:
            abort(422)

        return jsonify({
            'success': True,
            'delete': id
        }), 200

    #  Update Worker


@app.route('/inputs/<int:id>', methods=['PATCH'])
@requires_auth('patch:inputs')
def update_inputs(payload, id):
        data = request.get_json()
        input = Inputs.query.filter(Inputs.id == id).one_or_none()

        if not input:
            abort(404)

        try:
            updated_name = data.get('name', None)
            updated_qty = data.get('quantity', None)
            updated_metrics = data.get('metrics', None)
            updated_type = data.get('type', None)

            if updated_name:
                input.name = updated_name
            if updated_qty:
                input.phone_number = updated_qty
            if updated_metrics:
                input.metrics = updated_metrics
            if updated_type:
                input.type = updated_type

            input.update()

        except BaseException:
            abort(400)

        return jsonify({
            'success': True,
            'input': [input.format()]
        }), 200

    # Get Fields
@app.route('/fields', methods=['GET'])
@requires_auth('get:fields')
def get_fields(payload):
        fields = Fields.query.all()
        if not fields:
            abort(404)

        return jsonify({
            'success': True,
            'fields': [field.format() for field in fields]
        }), 200

    # Add Fields
@app.route('/fields', methods=['POST'])
@requires_auth('post:fields')
def create_fields(payload):
        data = request.get_json()
      
        try:
            new_name = data.get('name', None)
            new_size = data.get('size', None)
            print(new_name)
            print(new_size)

            fields = Fields(name=new_name, size=new_size)
            fields.insert()
        except Exception as e:
            print(e)
            abort(404)

        return jsonify({
            'success': True,
            'fields': fields.format()
        })

    # Delete Fields


@app.route('/fields/<id>', methods=['DELETE'])
@requires_auth('delete:fields')
def delete_fields(payload, id):
        field = Fields.query.filter(Fields.id == id).one_or_none()

        if not field:
            abort(404)
        try:
            field.delete()
        except BaseException:
            abort(400)

        return jsonify({
            'success': True,
            'delete': id
        }), 200


@app.route('/fields/<int:id>', methods=['PATCH'])
@requires_auth('patch:fields ')
def update_fields(payload, id):
        data = request.get_json()
        field = Fields.query.filter(Fields.id == id).one_or_none()

        if not field:
            abort(404)

        try:
            updated_name = data.get('name', None)
            updated_size = data.get('size', None)

            if updated_name:
                field.name = updated_name
            if updated_size:
                field.size = updated_size

            field.update()

        except BaseException:
            abort(400)

        return jsonify({
            'success': True,
            'field': [field.format()]
        }), 200

    # Error handlers for 400, 404, 422 and 500


@app.errorhandler(400)
def bad_request(error):
      return jsonify({
           'success': False,
           'error': 400,
                'message': 'bad request'
           }), 400


@app.errorhandler(500)
def server_error(error):
      return jsonify({
           'success': False,
           'error': 500,
                'message': 'server error'
           }), 500


@app.errorhandler(404)
def not_found(error):
          return jsonify({
               'success': False,
                'error': 404,
                'message': 'resource not found'
               }), 404


@app.errorhandler(422)
def unprocessable(error):
          return jsonify({
               'success': False,
                'error': 422,
                'message': 'unprocessable'
               }), 422


@app.errorhandler(AuthError)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
