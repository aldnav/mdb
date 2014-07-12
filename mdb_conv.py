
import sys
import csv
import pyodbc
import tablib


def main(argv):

	# mdb = 'Dengue2009.MDB'
	mdb = argv[0]
	drv = '{Microsoft Access Driver (*.mdb)}'
	pwd = ''

	# housekeeping
	databook = tablib.Databook()
	datasets = {}
	raw_objs = ['MSysNavPaneGroupToObjects', 'MSysAccessObjects', 'MSysQueries', 'MSysACEs', 'MSysObjects', 
	'MSysNavPaneGroups', 'MSysNavPaneObjectIDs', 'MSysNavPaneGroupCategories', 'MSysRelationships', 'MSysNameMap']

	con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(drv, mdb, pwd))
	cursor = con.cursor()

	print 'Exposing tables...',
	for row in cursor.tables():
		# if row.table_name in raw_objs:
		# 	continue
		datasets[row.table_name] = tablib.Dataset(title=row.table_name)
	print '\t\t[OK]'

	# Adding sheet headers
	print 'Preparing sheets...',
	for datasetname, dataset in datasets.items():
		dataset.headers = [row.column_name for row in cursor.columns(table=datasetname)]

	# # Adding datasheets to databook
	for dataset in datasets.values():
		databook.add_sheet(dataset)
	print '\t\t[OK]'

	# Normalize msys raw objects
	print 'Normalizing...',
	for obj in raw_objs:
		if obj in datasets.keys(): datasets.pop(obj, None)
	print '\t\t\t[OK]'

	print 'Populating data...',
	for datasetname, dataset in datasets.items():
		sql = 'SELECT * FROM %s' % datasetname
		try:
			cursor.execute(sql)	
			for row in cursor.fetchall():
				if row:
					# print datasetname, row
					try:
						dataset.append(row)
					except: pass
		except:
			pass
	print '\t\t[OK]'

	cursor.close()
	con.close()

	print 'Writing excel file...',
	with open(mdb + '.xls', 'wb') as f:
		f.write(databook.xls)
	print '\t\t[OK]'

if __name__ == '__main__':
	main(sys.argv[1:])
	# main(('Dengue2013.MDB',))