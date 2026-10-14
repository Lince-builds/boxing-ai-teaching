import unittest,tempfile,subprocess,sys,time,json,urllib.request,socket,concurrent.futures
from pathlib import Path
import app
class SampleTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.old=(app.DATA,app.DB);app.DATA=Path(self.tmp.name);app.DB=app.DATA/'test.sqlite3';app.initialize()
 def tearDown(self):app.DATA,app.DB=self.old;self.tmp.cleanup()
 def test_booking_duplicate_cancel(self):
  self.assertEqual(app.snapshot()['member']['available'],3)
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:r=list(pool.map(lambda _:app.book(),range(12)))
  self.assertEqual(len(set(x['id'] for x in r)),1);self.assertEqual(app.snapshot()['member']['reserved'],1)
  app.cancel(r[0]['id']);app.cancel(r[0]['id']);self.assertEqual(app.snapshot()['member']['available'],3);self.assertEqual(app.snapshot()['member']['used'],0)
 def test_saved_after_reopen(self):
  bid=app.book()['id'];app.initialize();self.assertEqual(app.snapshot()['bookings'][0]['id'],bid)
 def test_period_and_totals(self):
  s=app.summary();self.assertEqual(s['metrics'],{'completed_sessions':4,'cancelled_sessions':2,'active_members':3,'registered_members':4,'activity_coverage_percent':75.0,'course_sales_receipts_yuan':1500})
  self.assertNotIn('S07',s['evidence']['completed_session_ids']);self.assertNotIn('O03',s['evidence']['receipt_order_ids'])
 def test_reset_is_local(self):
  (app.DATA/'latest-report.json').write_text('{}');app.book();app.reset();self.assertEqual(app.snapshot()['bookings'],[]);self.assertTrue((app.DATA/'latest-report.json').exists())
 def test_unknown_cancel(self):
  with self.assertRaises(ValueError):app.cancel('missing')
 def test_question_boundary(self):
  s=app.make_prompt(app.summary(),'这周赚了多少利润？留存是不是提高了？');self.assertIn('09-08 00:00（不含）',s)
  self.assertIn('缺成本',s);self.assertIn('这周赚了多少利润',s)
if __name__=='__main__':unittest.main()
