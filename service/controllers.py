import datetime
from flask import request
from flask_restful import Resource
from openapi_core.shortcuts import RequestValidator
from openapi_core.wrappers.flask import FlaskOpenAPIRequest
# import psycopg2
#import sqlalchemy
import chords
import influx
from models import ChordsSite, ChordsIntrument, ChordsVariable
from common import utils, errors
#from service.models import db, LDAPConnection, TenantOwner, Tenant

# get the logger instance -
from common.logs import get_logger
logger = get_logger(__name__)


class ProjectsResource(Resource):
    """
    Work with Project objects
    """
    def get(self):
        return ""

    def post(self):
        return ""

class ProjectResource(Resource):
    """
    Work with Project objects
    """

    def get(self, project_id):
        return ""

    def put(self, project_id):
        return ""

    def delete(self, project_id):
        return ""

class SitesResource(Resource):
    """
    Work with Sites objects
    """

    #TODO metadata integration - need to use query, limit and offset
    def get(self, project_id):
        result,msg = chords.list_sites()
        return utils.ok(result=result,msg=msg)


    def post(self, project_id):
        logger.debug('omg')
        logger.debug(request.json)
        body = request.json
        postSite = ChordsSite("",body['site_name'],
                                body['latitude'],
                                body['longitude'],
                                body['elevation'],
                                body['description'])
        result, msg = chords.create_site(postSite)
        return utils.ok(result=result, msg=msg)


class SiteResource(Resource):
    """
    Work with Sites objects
    """

    def get(self, project_id, site_id):
        result,msg = chords.get_site(site_id)
        #logger.debug(resp)
        return utils.ok(result=result, msg=msg)

    def put(self, project_id, site_id):
        body = request.json
        putSite = ChordsSite(site_id,
                              body['site_name'],
                              body['latitude'],
                              body['longitude'],
                              body['elevation'],
                              body['description'])
        result, msg = chords.update_site(site_id, putSite)
        return utils.ok(result=result, msg=msg)

    def delete(self, project_id, site_id):
        result, msg = chords.delete_site(site_id)
        logger.debug(msg)
        return utils.ok(result='null', msg=f'Site {site_id} deleted.')


class InstrumentsResource(Resource):
    """
    Work with Instruments objects
    """
    def get(self,project_id,site_id):
        result,msg = chords.list_instruments()
        '''
        #logic to filter instruments based on site id
        filtered_res = []
        list_index = 0
        logger.debug(site_id)
        for i in range(len(result)):
            if (result[i]["site_id"] == int(site_id)):
                filtered_res.insert(list_index, result[i])
                list_index = list_index + 1
                logger.debug(filtered_res)
            if (len(filtered_res)!=0):
                return utils.ok(result=filtered_res, msg=msg)
            else:
                return utils.ok(result="null", msg=f'No instruments found with this site')
        '''
        return utils.ok(result=result, msg=msg)

    #TODO support bulk create operations
    def post(self, project_id, site_id):
        logger.debug(type(request.json))
        logger.debug(request.json)
        #TODO loop through list objects to support build operations
        if type(request.json) is dict:
            body = request.json
        else:
            body = request.json[0]
        logger.debug('before ChordsInstrument assignment')
        #id, site_id, name, sensor_id, topic_category_id, description, display_points, plot_offset_value, plot_offset_units, sample_rate_seconds):

        postInst = ChordsIntrument("",site_id,
                                    body['inst_name'],
                                    "",
                                    "",
                                    body['inst_description'],
                                    "120",
                                    "1",
                                    "weeks",
                                    "60")
        logger.debug('after ChordsInstrument assignment')
        result, msg = chords.create_instrument(postInst)
        return utils.ok(result=result, msg=f'Instrument created')


class InstrumentResource(Resource):
    """
    Work with Instruments objects
    """
    def get(self, project_id, site_id, instrument_id):
        result,msg = chords.get_instrument(instrument_id)
        logger.debug(site_id)
        return utils.ok(result=result, msg=msg)


    def put(self, project_id, site_id, instrument_id):
        logger.debug(type(request.json))
        logger.debug(request.json)
        #TODO loop through list objects to support buld operations
        if type(request.json) is dict:
            body = request.json
        else:
            body = request.json[0]
        putInst = ChordsIntrument(instrument_id,site_id,
                                    body['inst_name'],
                                    "",
                                    "",
                                    body['inst_description'],
                                    "",
                                    "",
                                    "",
                                    "")
        result, msg = chords.update_instrument(instrument_id, putInst)
        return utils.ok(result=result, msg=msg)


    def delete(self, project_id, site_id, instrument_id):
        result,msg = chords.delete_instrument(instrument_id)
        return utils.ok(result="null", msg=msg)


class VariablesResource(Resource):
    """
    Work with Variables objects
    """

    def get(self, project_id, site_id, instrument_id):
        result,msg = chords.list_variables()
        logger.debug(instrument_id)
        return utils.ok(result=result, msg=msg)


    def post(self, project_id, site_id, instrument_id):
        #logger.debug(type(request.json))
        logger.debug(request.json)
        #TODO loop through list objects to support buld operations
        if type(request.json) is dict:
            body = request.json
        else:
            body = request.json[0]
        # id, name, instrument_id, shortname, commit
        postInst = ChordsVariable("test",instrument_id,
                                    body['var_name'],
                                    body['shortname'],
                                    "")
        logger.debug(postInst)
        result, msg = chords.create_variable(postInst)
        logger.debug(result)
        return utils.ok(result=result, msg=msg)


class VariableResource(Resource):
    """
    Work with Variables objects
    """
    def get(self, project_id, site_id, instrument_id, variable_id):
        result,msg = chords.get_variable(variable_id)
        logger.debug(result)
        return utils.ok(result=result, msg=msg)


    def put(self,project_id, site_id, instrument_id,  variable_id):
        logger.debug(type(request.json))
        logger.debug(request.json)
        #TODO loop through list objects to support buld operations
        if type(request.json) is dict:
            body = request.json
        else:
            body = request.json[0]
        # id, name, instrument_id, shortname, commit
        putInst = ChordsVariable(variable_id,instrument_id,
                                    body['var_name'],
                                    body['shortname'],
                                    "")
        logger.debug(putInst)
        result,msg = chords.update_variable(variable_id,putInst)
        logger.debug(result)
        return utils.ok(result=result, msg=msg)

    def delete(self, project_id, site_id, instrument_id, variable_id):
        result,msg = chords.delete_variable(variable_id)
        logger.debug(result)
        return utils.ok(result=result, msg=msg)

class MeasurementsResource(Resource):
    """
    Work with Measurements objects
    """
    #
    def get(self, project_id, site_id, instrument_id):
        logger.debug("top of GET /measurements")
        result,msg = chords.get_measurements(instrument_id)
        logger.debug(result)
        return utils.ok(result=result, msg=msg)

    #at the moment expects some like
    #http://localhost:5000/v3/streams/measurements?instrument_id=1&vars[]={"somename":1.0}&vars[]={"other":2.0}
    #will need to adjust when openAPI def is final for measurement
    def post(self, project_id, site_id, instrument_id):
        body = request.json
        logger.debug(body)
        #expects instrument_id=1&vars[]={"somename":1.0}&vars[]={"other":2.0} in the request.args
        resp = chords.create_measurement(body)
        logger.debug(resp)
        return resp


class MeasurementResource(Resource):
    """
    Work with Measurements objects
    """

    def get(self, measurement_id):
        logger.debug("top of GET /measurements/{measurement_id}")

    def put(self, measurement_id):
        logger.debug("top of PUT /measurements/{measurement_id}")

    def delete(self, measurement_id):
        logger.debug("top of DELETE /measurements/{measurement_id}")

class StreamsResource(Resource):
    """
    Work with Streams objects
    """

    def get(self):
        logger.debug("top of GET /streams")

    def post(self):
        logger.debug("top of POST /streams")


class StreamResource(Resource):
    """
    Work with Streams objects
    """

    def get(self, stream_id):
        logger.debug("top of GET /streams/{stream_id}")

    def put(self, stream_id):
        logger.debug("top of PUT /streams/{stream_id}")

    def delete(self, stream_id):
        logger.debug("top of DELETE /streams/{stream_id}")

class InfluxResource(Resource):

    #Expect fields[] parameters
    #EXAMPLE: fields[]={"inst":1}&fields[]={"var":1}
    def get(self):
        logger.debug(request.args)
        field_list = request.args.getlist('fields[]')
        #expects instrument_id=1&vars[]={"somename":1.0}&vars[]={"other":2.0} in the request.args
        resp = influx.query_measurments(field_list)
        logger.debug(resp)
        return resp

    def post(self):
        logger.debug(request.args)
        #expects instrument_id=1&vars[]={"somename":1.0}&vars[]={"other":2.0} in the request.args
        resp = influx.create_measurement(request.args.get('site_id'), request.args.get('inst_id'), request.args.get('var_id'),  float(request.args.get('value')), request.args.get('timestamp'), )
        logger.debug(resp)
        return resp

#class ChannelResource(Resource):


#class ChannelsResource(Resource):