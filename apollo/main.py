import interpreter
import settings
import dbaccess
import problem
import translator

st = settings.Settings('/Users/thyago/Dropbox/Temp/test.ini')
st.load()
db = dbaccess.DataAccess(st.get('db_path'))
pm = problem.ProblemManager(settings=st, db=db)
t = translator.Translator(pm)

st.translator = t

it = interpreter.Interpreter(settings=st, database=db)
it.cmdloop('Apollo (Development v0.0.1) - Designed for Python 3')
