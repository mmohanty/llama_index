from flask import Flask, jsonify, request
from peewee import *
from flask_cors import CORS, cross_origin
from playhouse.shortcuts import model_to_dict, dict_to_model


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

database = "../../data/sqlite/contracts.db"
db = SqliteDatabase(database)


class Contract(Model):
    id = AutoField()
    contract_id = CharField()
    vendor_name = CharField()
    contract_value = CharField()
    start_date = CharField()
    end_date = CharField()
    renewal_date = CharField()

    class Meta:
        database = db
        table_name = 'contract'


@app.get('/contract')
@cross_origin()
def get():
    query = Contract.select(Contract).order_by(Contract.id).dicts()
    return list(query)


@app.patch('/contract')
@cross_origin()
def patch():
    data = request.get_json()
    id = request.get_json()['id']

    try:
        query = Contract.select(Contract).where(Contract.id == id)
        existingRecord = query.get()
        # update
        existingRecord.vendor_name = existingRecord.vendor_name if existingRecord.vendor_name == request.get_json()[
            'vendor_name'] else request.get_json()['vendor_name']
        existingRecord.contract_id = existingRecord.contract_id if existingRecord.contract_id == request.get_json()[
            'contract_id'] else request.get_json()['contract_id']
        existingRecord.start_date = existingRecord.start_date if existingRecord.start_date == request.get_json()[
            'start_date'] else request.get_json()['start_date']
        existingRecord.end_date = existingRecord.end_date if existingRecord.end_date == request.get_json()[
            'end_date'] else request.get_json()['end_date']
        existingRecord.renewal_date = existingRecord.renewal_date if existingRecord.renewal_date == request.get_json()[
            'renewal_date'] else request.get_json()['renewal_date']
        existingRecord.contract_value = existingRecord.contract_value if existingRecord.contract_value == \
                                                                         request.get_json()['contract_value'] else \
            request.get_json()['contract_value']
        Contract.save(existingRecord)
    except DoesNotExist:
        # Insert
        Contract.create(contract_id=request.get_json()['contract_id'],
                        vendor_name=request.get_json()['vendor_name'],
                        contract_value=request.get_json()['contract_value'],
                        start_date=request.get_json()['start_date'],
                        end_date=request.get_json()['end_date'],
                        renewal_date=request.get_json()['renewal_date'])

    q = Contract.select(Contract).where(Contract.contract_id == request.get_json()['contract_id']).get()
    return model_to_dict(q)


@app.delete('/contract/<rowId>')
@cross_origin()
def delete(rowId):
    q = Contract.select(Contract).where(Contract.id == rowId).get()
    Contract.delete_by_id(rowId)
    return model_to_dict(q)


if __name__ == '__main__':
    app.run()  # run our Flask app
