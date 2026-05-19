from django.urls import path
from django.contrib.auth import views as auth_views  # <--- TAMBAHKAN BARIS INI
from . import views

from django.conf import settings          # TAMBAHKAN
from django.conf.urls.static import static # TAMBAHKAN


app_name = 'pemeliharaan'

urlpatterns = [
    # === AUTH ROUTES ===
    path('login/', auth_views.LoginView.as_view(template_name='pemeliharaan/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Kendaraan
    path('kendaraan/', views.kendaraan_list, name='kendaraan_list'),
    path('kendaraan/tambah/', views.kendaraan_create, name='kendaraan_create'),
    path('kendaraan/<int:pk>/edit/', views.kendaraan_update, name='kendaraan_update'),
    path('kendaraan/<int:pk>/hapus/', views.kendaraan_delete, name='kendaraan_delete'),
    path('kendaraan/<int:pk>/', views.kendaraan_detail, name='kendaraan_detail'),

    # Bengkel
    path('bengkel/', views.bengkel_list, name='bengkel_list'),
    path('bengkel/tambah/', views.bengkel_create, name='bengkel_create'),
    path('bengkel/<int:pk>/edit/', views.bengkel_update, name='bengkel_update'),
    path('bengkel/<int:pk>/hapus/', views.bengkel_delete, name='bengkel_delete'),

    # Spare Part
    path('sparepart/', views.sparepart_list, name='sparepart_list'),
    path('sparepart/tambah/', views.sparepart_create, name='sparepart_create'),
    path('sparepart/<int:pk>/edit/', views.sparepart_update, name='sparepart_update'),
    path('sparepart/<int:pk>/hapus/', views.sparepart_delete, name='sparepart_delete'),

    # Jasa Servis
    path('jasa-servis/', views.jasaservis_list, name='jasaservis_list'),
    path('jasa-servis/tambah/', views.jasaservis_create, name='jasaservis_create'),
    path('jasa-servis/<int:pk>/edit/', views.jasaservis_update, name='jasaservis_update'),
    path('jasa-servis/<int:pk>/hapus/', views.jasaservis_delete, name='jasaservis_delete'),

    # Pemeliharaan
    path('pemeliharaan/', views.pemeliharaan_list, name='pemeliharaan_list'),
    path('pemeliharaan/tambah/', views.pemeliharaan_create, name='pemeliharaan_create'),
    path('pemeliharaan/<int:pk>/edit/', views.pemeliharaan_update, name='pemeliharaan_update'),
    path('pemeliharaan/<int:pk>/hapus/', views.pemeliharaan_delete, name='pemeliharaan_delete'),
    path('pemeliharaan/<int:pk>/', views.pemeliharaan_detail, name='pemeliharaan_detail'),
    path('pemeliharaan/<int:pk>/kuitansi/', views.export_kuitansi_excel, name='export_kuitansi_excel'), # <-- TAMBAHKAN INI
    path('pemeliharaan/<int:pk>/hapus-sparepart/<int:detail_pk>/',
         views.hapus_detail_sparepart, name='hapus_detail_sparepart'),
    path('pemeliharaan/<int:pk>/hapus-jasaservis/<int:detail_pk>/',
         views.hapus_detail_jasaservis, name='hapus_detail_jasaservis'),

    # Konsumsi Bensin
    path('bensin/', views.bensin_list, name='bensin_list'),
    path('bensin/tambah/', views.bensin_create, name='bensin_create'),
    path('bensin/<int:pk>/edit/', views.bensin_update, name='bensin_update'),
    path('bensin/<int:pk>/hapus/', views.bensin_delete, name='bensin_delete'),

     # TAMBAHKAN BARIS INI
    path('bensin/<int:pk>/struk/', views.export_struk_bensin_pdf, name='export_struk_bensin_pdf'),

    # Laporan
    path('laporan/export-excel/', views.export_laporan_excel, name='export_laporan_excel'), # <-- TARUH INI DULU
    path('laporan/', views.laporan, name='laporan'),
]