import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('seed',ROOT/'scripts/seed.py')
seed=importlib.util.module_from_spec(spec); spec.loader.exec_module(seed)
class SeedTests(unittest.TestCase):
 def test_scenarios(self):
  for scenario, expected in json.loads((ROOT/'validation/expected-results.json').read_text()).items():
   events=seed.generate(scenario); rows,errors=seed.consume(events,scenario)
   self.assertEqual(seed.metrics(events,rows,errors),expected)
   self.assertEqual(events,seed.generate(scenario))
 def test_offset_and_boundary(self):
  events=seed.generate('incident'); rows,_=seed.consume(events,'incident')
  self.assertEqual(events[1499]['schemaVersion'],1)
  self.assertEqual(events[1500]['schemaVersion'],2)
  self.assertEqual(rows[0][5]-seed.datetime.fromisoformat(events[0]['occurredAt']),seed.timedelta(hours=2))
  self.assertEqual(events[3000],events[0])
  self.assertNotEqual(rows[3000][0],rows[0][0])
if __name__=='__main__': unittest.main()
