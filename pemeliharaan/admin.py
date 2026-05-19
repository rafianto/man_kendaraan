from django.contrib import admin
from .models import (
    Kendaraan, Bengkel, SparePart, JasaServis,
    Pemeliharaan, DetailSparePart, DetailJasaServis
)


class DetailSparePartInline(admin.TabularInline):
    model = DetailSparePart
    extra = 1
    readonly_fields = ('subtotal',)


class DetailJasaServisInline(admin.TabularInline):
    model = DetailJasaServis
    extra = 1


@admin.register(Kendaraan)
class KendaraanAdmin(admin.ModelAdmin):
    list_display = ('nomor_polisi', 'merk', 'tipe', 'jenis', 'pemilik_pengguna', 'aktif')
    list_filter = ('jenis', 'aktif', 'tahun_pembuatan')
    search_fields = ('nomor_polisi', 'merk', 'tipe', 'pemilik_pengguna')


@admin.register(Bengkel)
class BengkelAdmin(admin.ModelAdmin):
    list_display = ('nama_bengkel', 'pemilik', 'kota', 'no_telp')
    search_fields = ('nama_bengkel', 'pemilik', 'kota')


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('kode', 'nama_sparepart', 'harga')
    search_fields = ('kode', 'nama_sparepart')


@admin.register(JasaServis)
class JasaServisAdmin(admin.ModelAdmin):
    list_display = ('kode', 'nama_jasa', 'biaya')
    search_fields = ('kode', 'nama_jasa')


@admin.register(Pemeliharaan)
class PemeliharaanAdmin(admin.ModelAdmin):
    list_display = ('no_servis', 'kendaraan', 'bengkel', 'tanggal_servis',
                    'total_biaya_sparepart', 'total_biaya_jasa', 'total_biaya')
    list_filter = ('tanggal_servis', 'kendaraan__jenis', 'bengkel')
    search_fields = ('no_servis', 'kendaraan__nomor_polisi')
    readonly_fields = ('no_servis', 'total_biaya_sparepart', 'total_biaya_jasa', 'total_biaya')
    inlines = [DetailSparePartInline, DetailJasaServisInline]


@admin.register(DetailSparePart)
class DetailSparePartAdmin(admin.ModelAdmin):
    list_display = ('pemeliharaan', 'sparepart', 'jumlah', 'harga_satuan', 'subtotal')
    readonly_fields = ('subtotal',)


@admin.register(DetailJasaServis)
class DetailJasaServisAdmin(admin.ModelAdmin):
    list_display = ('pemeliharaan', 'jasa_servis', 'biaya')