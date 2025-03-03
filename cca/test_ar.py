import os
import sys
import django
from models import hasil_cca, hasil_detail_cca, matrix2_cr, matrix_hasil_cr

sys.path.insert(0, os.path.abspath('.'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'eauctions.settings'
django.setup()

hasil = hasil_cca.objects.all().filter(item_lelang = 70).distinct('bidder')
for a in hasil:
    m = matrix2_cr.objects.all().filter(parent__item_lelang = 70, parent__bidder=a.bidder).distinct('kombinasi').order_by('kombinasi','-parent__round')
    print(m)