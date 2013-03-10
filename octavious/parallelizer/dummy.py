from octavious.parallelizer import Parallelizer


class DummyParallelizer(Parallelizer):   

    def parallelize(self, processors, input=None, callback=None):
    	results = []
        for processor in processors:
        	output = processor(input)
        	results.append(output)
        	if callback:
        		callback(output)
        return results

parallelizer = DummyParallelizer
