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
class LiveDemoTests(unittest.TestCase):
 def test_three_deliveries_two_events(self):
  events=seed.live_events()
  self.assertEqual(events[1], events[2])
  expected={'baseline': (2, 0, 3000), 'incident': (3, 2, 5000)}
  for scenario, (count, missing, cents) in expected.items():
   rows, errors=seed.consume(events, scenario)
   self.assertEqual(len(rows), count)
   self.assertEqual(len(errors), missing)
   self.assertEqual(sum(r[4] for r in rows), cents)
   self.assertEqual(sum(r[5] != seed.datetime.fromisoformat(events[r[0]-1]['occurredAt']) for r in rows), missing)

if __name__=='__main__': unittest.main()
