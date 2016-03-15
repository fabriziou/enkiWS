import datetime
import random
import webapp2_extras.security

from google.appengine.ext import ndb

from enki.modelrestapiconnecttoken import EnkiModelRestAPIConnectToken
from enki.modelrestapidatastore import EnkiModelRestAPIDataStore


MAX_AGE = 5    # in minutes, duration of a connection token validity
DATASTORE_EXPIRY_DEFAULT = 86400    # 24h
DATASTORE_NON_EXPIRING = 3154000000 # 100 years
DATASTORE_NON_EXPIRING_REFRESH = DATASTORE_NON_EXPIRING / 2


def generate_connect_code():
	return webapp2_extras.security.generate_random_string( length = 5, pool = webapp2_extras.security.UPPERCASE_ALPHANUMERIC )


def generate_auth_token():
	return webapp2_extras.security.generate_random_string( length = 42, pool = webapp2_extras.security.ALPHANUMERIC )


def cleanup_and_get_new_connection_token( user_id ):
	# note: ensure user is logged in and has display name before calling this function
	if user_id:
		# delete any existing connect token for the user
		ndb.delete_multi_async( fetch_EnkiModelRestAPIConnectToken_by_user( user_id ))
		# create a new token and return it
		token = generate_connect_code()
		entity = EnkiModelRestAPIConnectToken( token = token, user_id = int( user_id ))
		entity.put()
		return token
	return None


def refresh_EnkiModelRestAPIConnectToken_non_expiring():
	likelyhood = 10 # occurs with a probability of 1%
	number = random.randint( 1, 1000 )
	if number < likelyhood:
		list = fetch_EnkiModelRestAPIDataStore_non_expiring()
		for item in list:
			item.time_expires = datetime.datetime.now() + datetime.timedelta( seconds = DATASTORE_NON_EXPIRING )
		ndb.put_multi_async( list )


#=== QUERIES ==================================================================


def get_EnkiModelRestAPIConnectToken_by_token_user_id_valid_age( token, user_id ):
	entity = EnkiModelRestAPIConnectToken.query( ndb.AND( EnkiModelRestAPIConnectToken.token == token,
	                                                      EnkiModelRestAPIConnectToken.user_id == user_id,
	                                                      EnkiModelRestAPIConnectToken.time_created > ( datetime.datetime.now( ) - datetime.timedelta( minutes = MAX_AGE )))).get()
	return entity


def fetch_EnkiModelRestAPIConnectToken_by_user( user_id ):
	list = EnkiModelRestAPIConnectToken.query( EnkiModelRestAPIConnectToken.user_id == user_id ).fetch( keys_only = True )
	return list


def fetch_EnkiModelRestAPIConnectToken_by_app_id_data_key_read_access( app_id, data_key, read_access ):
	list = EnkiModelRestAPIDataStore.query( ndb.AND( EnkiModelRestAPIDataStore.app_id == app_id,
	                                                 EnkiModelRestAPIDataStore.data_key == data_key,
	                                                 EnkiModelRestAPIDataStore.read_access == read_access )).fetch()
	return list


def fetch_EnkiModelRestAPIConnectToken_expired():
	list = EnkiModelRestAPIConnectToken.query( EnkiModelRestAPIConnectToken.time_created < ( datetime.datetime.now( ) - datetime.timedelta( minutes = MAX_AGE ))).fetch( keys_only = True )
	return list


def get_EnkiModelRestAPIDataStore_by_user_id_app_id_data_key( user_id, app_id, data_key ):
	entity = EnkiModelRestAPIDataStore.query( ndb.AND( EnkiModelRestAPIDataStore.user_id == user_id,
	                                                   EnkiModelRestAPIDataStore.app_id == app_id,
	                                                   EnkiModelRestAPIDataStore.data_key == data_key )).get()
	return entity


def get_EnkiModelRestAPIDataStore_by_user_id_app_id_data_key_read_access( user_id, app_id, data_key, read_access ):
	entity = EnkiModelRestAPIDataStore.query( ndb.AND( EnkiModelRestAPIDataStore.user_id == user_id,
	                                                   EnkiModelRestAPIDataStore.app_id == app_id,
	                                                   EnkiModelRestAPIDataStore.data_key == data_key,
	                                                   EnkiModelRestAPIDataStore.read_access == read_access )).get()
	return entity


def fetch_EnkiModelRestAPIDataStore_by_user_id_app_id_data_key( user_id, app_id, data_key ):
	list = EnkiModelRestAPIDataStore.query( ndb.AND( EnkiModelRestAPIDataStore.user_id == user_id,
	                                                 EnkiModelRestAPIDataStore.app_id == app_id,
	                                                 EnkiModelRestAPIDataStore.data_key == data_key )).fetch( keys_only = True )
	return list


def fetch_EnkiModelRestAPIDataStore_expired():
	list = EnkiModelRestAPIDataStore.query( EnkiModelRestAPIDataStore.time_expires < datetime.datetime.now()).fetch( keys_only = True )
	return list


def fetch_EnkiModelRestAPIDataStore_non_expiring():
	list = EnkiModelRestAPIDataStore.query( EnkiModelRestAPIDataStore.time_expires > ( datetime.datetime.now() + datetime.timedelta( seconds = DATASTORE_NON_EXPIRING_REFRESH ))).fetch()
	return list
