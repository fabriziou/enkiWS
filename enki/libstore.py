import webapp2_extras.security

from google.appengine.ext import ndb

from enki.modelproductkey import EnkiModelProductKey


LICENCE_KEY_LENGTH = 15
LICENCE_KEY_DASHES_LENGTH = LICENCE_KEY_LENGTH + 2  # licence including two inserted dashes
SEPARATOR_LICENCE_KEYS = '\n'


def generate_licence_key():
	code = webapp2_extras.security.generate_random_string( length = LICENCE_KEY_LENGTH, pool = webapp2_extras.security.UPPERCASE_ALPHANUMERIC )
	return code


def insert_dashes_5_10( string ):
	result_10 = string[:10] + '-' + string[10:]
	result = result_10[:5] + '-' + result_10[5:]
	return result


def generate_licence_keys( quantity ):
	licence_keys = ''
	if quantity:
		quantity = int( quantity )
		while quantity > 0:
			licence_keys += insert_dashes_5_10( generate_licence_key()) + SEPARATOR_LICENCE_KEYS
			quantity -= 1
	return licence_keys


#=== QUERIES ==================================================================


def get_EnkiProductKey_by_licence_key( licence_key ):
	entity = EnkiModelProductKey.query( EnkiModelProductKey.licence_key == licence_key.replace( '-', '' ) ).get()
	return entity


def exist_EnkiProductKey_product_activated_by( user_id, product_name ):
	count = EnkiModelProductKey.query( ndb.AND( EnkiModelProductKey.activated_by_user == user_id,
	                                            EnkiModelProductKey.product_name == product_name )).count( 1 )
	return count > 0


def fetch_EnkiProductKey_by_purchaser( user_id ):
	list = EnkiModelProductKey.query( EnkiModelProductKey.purchaser_user_id == user_id ).order( EnkiModelProductKey.product_name ).fetch()
	return list


def fetch_EnkiProductKey_by_activator( user_id ):
	list = EnkiModelProductKey.query( EnkiModelProductKey.activated_by_user == user_id ).order( EnkiModelProductKey.product_name ).fetch()
	return list


def fetch_EnkiProductKey_by_activator_products_list( user_id, products_list ):
	list = EnkiModelProductKey.query( ndb.AND( EnkiModelProductKey.activated_by_user == user_id,
	                                           EnkiModelProductKey.product_name.IN( products_list )
	                                           )).fetch()
	return list
