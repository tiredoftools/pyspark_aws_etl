import sys


class etl():
    def run(self, sc, **kwargs):
        raise NotImplementedError

    def runner(self, sc, sc_sql):
        self.sc = sc
        self.sc_sql = sc_sql
        # import ipdb; ipdb.set_trace()
        run_args = {}
        for item in self.INPUTS.keys():
            # run_args[item] = sc.textFile(self.INPUTS[item]['path'])
            if self.INPUTS[item]['type'] == 'txt':
                run_args[item] = sc.textFile(self.INPUTS[item]['path'])
            elif self.INPUTS[item]['type'] == 'parquet':
                run_args[item] = sc_sql.read.parquet(self.INPUTS[item]['path'])
                run_args[item].createOrReplaceTempView(item)

        output = self.run(**run_args)
#        output.saveAsTextFile(self.OUTPUT['path'])
        if self.OUTPUT['type'] == 'txt':
            output.saveAsTextFile(self.OUTPUT['path'])
        elif self.OUTPUT['type'] == 'parquet':
            output.write.parquet(self.OUTPUT['path'])
        elif self.OUTPUT['type'] == 'csv':
            output.write.csv(self.OUTPUT['path'])

        print 'Wrote output to ',self.OUTPUT['path']
        return output

    # def query2(self, **kwargs):
    def query(self, query_str):
        print 'Query string:', query_str
        return self.sc_sql.sql(query_str)



def launch(classname, appName, app_file, aws):
    process = sys.argv[1] if len(sys.argv) > 1 else 'locally'

    if process == 'locally':
        from pyspark import SparkContext
        from pyspark.sql import SQLContext
        sc = SparkContext(appName=appName)
        sc_sql = SQLContext(sc)
        classname().runner(sc, sc_sql)
    elif process == 'clusterly':
        from core.run import DeployPySparkScriptOnAws
        DeployPySparkScriptOnAws(app_file=app_file, setup=aws).run()
