import unittest


loader = unittest.TestLoader()
loader.testMethodPrefix = "test"  # default value is "test"

suite1 = loader.discover('.', pattern="test*.py")
alltests = unittest.TestSuite(suite1)
unittest.TextTestRunner(verbosity=2).run(alltests)
