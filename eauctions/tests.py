import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eauctions.settings")
django.setup()

from smra2 import tasks
from smra2 import models
from django.utils import timezone
from datetime import datetime, timedelta
import argparse


detail_itemlelang = 113

def test_mulai():
    mulai = timezone.localtime()
    akhir = mulai + timedelta(minutes=5)
    models.round_smra2.objects.filter(item=detail_itemlelang).update(status_round='STA')
    tasks.mulai(detail_itemlelang,1, mulai.strftime("%d/%m/%Y %H:%M:00"), akhir.strftime("%d/%m/%Y %H:%M:00"), verbose_name="Memulai Putaran", schedule=mulai)

def run_specific_test(test_name):
    """Run a specific test based on the provided name."""
    if test_name == "mulai":
        print("Running 'Mulai'...")
        test_mulai()
    else:
        print(f"No test found with the name: {test_name}")

def main():
    parser = argparse.ArgumentParser(description="Script to run Django environment tasks.")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the test function instead of the main function."
    )
    args = parser.parse_args()
    if args.all:
        run_all_tests()
    elif args.test:
        run_specific_test(args.test)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()




class BackgroundTaskTestCase(TestCase):
    @property
    def detail_itemlelang(self):
        return 113
    
    def test_mulai(self):
        mulai = timezone.localtime()
        akhir = mulai + timedelta(minutes=5)
        models.round_smra2.objects.filter(item=self.detail_itemlelang).update(status_round='STA')
        tasks.mulai(self.detail_itemlelang,1, mulai.strftime("%d/%m/%Y %H:%M:00"), akhir.strftime("%d/%m/%Y %H:%M:00"), verbose_name="Memulai Putaran", schedule=mulai)
  
