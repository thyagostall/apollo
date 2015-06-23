from data import DataManager
from dbaccess import DataAccess

dao = DataAccess('/Users/thyago/proj/apollo/db/baseline.db')
dmg = DataManager(dao)
