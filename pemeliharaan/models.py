from django.db import models
from django.urls import reverse

import os
from django.db import models
from django.urls import reverse

def kendaraan_foto_path(instance, filename):
    nopol = instance.nomor_polisi.replace(' ', '_')
    return f'kendaraan/{nopol}/{filename}'

JENIS_KENDARAAN = [
    ('mobil', 'Mobil'),
    ('motor', 'Motor'),
    ('sepeda_listrik', 'Sepeda Listrik'),
]

class Kendaraan(models.Model):
    jenis = models.CharField('Jenis Kendaraan', max_length=20, choices=JENIS_KENDARAAN)
    nomor_polisi = models.CharField('Nomor Polisi', max_length=20, unique=True)
    merk = models.CharField('Merk', max_length=100)
    tipe = models.CharField('Tipe/Model', max_length=100)
    tahun_pembuatan = models.PositiveIntegerField('Tahun Pembuatan')
    warna = models.CharField('Warna', max_length=50)
    no_rangka = models.CharField('Nomor Rangka', max_length=100, blank=True, default='')
    no_mesin = models.CharField('Nomor Mesin', max_length=100, blank=True, default='')
    pemilik_pengguna = models.CharField('Pemilik/Pengguna', max_length=150)
    
    # PASTIKAN BARIS INI BENAR-BENAR ADA DAN SEJAJAR DENGAN FIELD LAINNYA
    foto = models.ImageField('Foto Kendaraan', upload_to=kendaraan_foto_path, blank=True, null=True)
    
    keterangan = models.TextField('Keterangan', blank=True, default='')
    aktif = models.BooleanField('Aktif', default=True)
    tanggal_input = models.DateTimeField('Tanggal Input', auto_now_add=True)

    class Meta:
        app_label = 'pemeliharaan'
        ordering = ['nomor_polisi']
        verbose_name = 'Kendaraan'
        verbose_name_plural = 'Data Kendaraan'

    def __str__(self):
        return f"{self.nomor_polisi} - {self.merk} {self.tipe}"

    def get_absolute_url(self):
        return reverse('pemeliharaan:kendaraan_detail', kwargs={'pk': self.pk})

    # ... property total_biaya_semua, dll biarkan seperti biasa ...

class Bengkel(models.Model):
    nama_bengkel = models.CharField('Nama Bengkel', max_length=200)
    pemilik = models.CharField('Pemilik', max_length=150)
    alamat = models.TextField('Alamat')
    kota = models.CharField('Kota', max_length=100)
    no_telp = models.CharField('No. Telepon', max_length=20)
    jenis_kendaraan = models.CharField(
        'Jenis Kendaraan Ditangani', max_length=200,
        help_text='Pisahkan dengan koma, cth: Mobil, Motor'
    )
    keterangan = models.TextField('Keterangan', blank=True, default='')
    tanggal_input = models.DateTimeField('Tanggal Input', auto_now_add=True)

    class Meta:
        ordering = ['nama_bengkel']
        verbose_name = 'Bengkel'
        verbose_name_plural = 'Data Bengkel'

    def __str__(self):
        return self.nama_bengkel

    def get_absolute_url(self):
        return reverse('pemeliharaan:bengkel_list')


class SparePart(models.Model):
    kode = models.CharField('Kode', max_length=50, unique=True)
    nama_sparepart = models.CharField('Nama Spare Part', max_length=200)
    harga = models.DecimalField('Harga Satuan', max_digits=12, decimal_places=2)
    keterangan = models.TextField('Keterangan', blank=True, default='')
    tanggal_input = models.DateTimeField('Tanggal Input', auto_now_add=True)

    class Meta:
        ordering = ['kode']
        verbose_name = 'Spare Part'
        verbose_name_plural = 'Data Spare Part'

    def __str__(self):
        return f"{self.kode} - {self.nama_sparepart}"

    def get_absolute_url(self):
        return reverse('pemeliharaan:sparepart_list')


class JasaServis(models.Model):
    kode = models.CharField('Kode', max_length=50, unique=True)
    nama_jasa = models.CharField('Nama Jasa', max_length=200)
    biaya = models.DecimalField('Biaya', max_digits=12, decimal_places=2)
    keterangan = models.TextField('Keterangan', blank=True, default='')
    tanggal_input = models.DateTimeField('Tanggal Input', auto_now_add=True)

    class Meta:
        ordering = ['kode']
        verbose_name = 'Jasa Servis'
        verbose_name_plural = 'Data Jasa Servis'

    def __str__(self):
        return f"{self.kode} - {self.nama_jasa}"

    def get_absolute_url(self):
        return reverse('pemeliharaan:jasaservis_list')


class Pemeliharaan(models.Model):
    no_servis = models.CharField('No. Servis', max_length=50, unique=True)
    kendaraan = models.ForeignKey(
        Kendaraan, on_delete=models.PROTECT, verbose_name='Kendaraan'
    )
    bengkel = models.ForeignKey(
        Bengkel, on_delete=models.PROTECT, verbose_name='Bengkel'
    )
    tanggal_servis = models.DateField('Tanggal Servis')
    km_saat_servis = models.PositiveIntegerField('KM Saat Servis', blank=True, null=True)
    keterangan = models.TextField('Keterangan', blank=True, default='')
    total_biaya_sparepart = models.DecimalField(
        'Total Biaya Spare Part', max_digits=14, decimal_places=2, default=0
    )
    total_biaya_jasa = models.DecimalField(
        'Total Biaya Jasa', max_digits=14, decimal_places=2, default=0
    )
    total_biaya = models.DecimalField(
        'Total Biaya', max_digits=14, decimal_places=2, default=0
    )
    tanggal_input = models.DateTimeField('Tanggal Input', auto_now_add=True)
    tanggal_update = models.DateTimeField('Tanggal Update', auto_now=True)

    class Meta:
        ordering = ['-tanggal_servis', '-no_servis']
        verbose_name = 'Pemeliharaan'
        verbose_name_plural = 'Data Pemeliharaan'

    def __str__(self):
        return self.no_servis

    def save(self, *args, **kwargs):
        if not self.no_servis:
            import datetime
            from django.db.models import Max
            today = datetime.date.today()
            prefix = f"SRV-{today.strftime('%Y%m%d')}"
            last = Pemeliharaan.objects.filter(
                no_servis__startswith=prefix
            ).aggregate(max_no=Max('no_servis'))['max_no']
            if last:
                num = int(last.split('-')[-1]) + 1
            else:
                num = 1
            self.no_servis = f"{prefix}-{num:03d}"
        super().save(*args, **kwargs)

    def hitung_total(self):
        """Hitung ulang total biaya dari detail sparepart dan jasa."""
        total_sp = self.detail_sparepart.aggregate(
            total=models.Sum('subtotal')
        )['total'] or 0
        total_js = self.detail_jasaservis.aggregate(
            total=models.Sum('biaya')
        )['total'] or 0
        self.total_biaya_sparepart = total_sp
        self.total_biaya_jasa = total_js
        self.total_biaya = total_sp + total_js
        Pemeliharaan.objects.filter(pk=self.pk).update(
            total_biaya_sparepart=total_sp,
            total_biaya_jasa=total_js,
            total_biaya=total_sp + total_js,
        )

    def get_absolute_url(self):
        return reverse('pemeliharaan:pemeliharaan_detail', kwargs={'pk': self.pk})


class DetailSparePart(models.Model):
    pemeliharaan = models.ForeignKey(
        Pemeliharaan, on_delete=models.CASCADE,
        related_name='detail_sparepart', verbose_name='Pemeliharaan'
    )
    sparepart = models.ForeignKey(
        SparePart, on_delete=models.PROTECT, verbose_name='Spare Part'
    )
    jumlah = models.PositiveIntegerField('Jumlah', default=1)
    harga_satuan = models.DecimalField('Harga Satuan', max_digits=12, decimal_places=2)
    subtotal = models.DecimalField('Subtotal', max_digits=14, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Detail Spare Part'
        verbose_name_plural = 'Detail Spare Part'

    def __str__(self):
        return f"{self.pemeliharaan.no_servis} - {self.sparepart.nama_sparepart}"

    def save(self, *args, **kwargs):
        self.subtotal = self.jumlah * self.harga_satuan
        super().save(*args, **kwargs)
        self.pemeliharaan.hitung_total()

    def delete(self, *args, **kwargs):
        pem = self.pemeliharaan
        super().delete(*args, **kwargs)
        pem.hitung_total()


class DetailJasaServis(models.Model):
    pemeliharaan = models.ForeignKey(
        Pemeliharaan, on_delete=models.CASCADE,
        related_name='detail_jasaservis', verbose_name='Pemeliharaan'
    )
    jasa_servis = models.ForeignKey(
        JasaServis, on_delete=models.PROTECT, verbose_name='Jasa Servis'
    )
    biaya = models.DecimalField('Biaya', max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Detail Jasa Servis'
        verbose_name_plural = 'Detail Jasa Servis'

    def __str__(self):
        return f"{self.pemeliharaan.no_servis} - {self.jasa_servis.nama_jasa}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pemeliharaan.hitung_total()

    def delete(self, *args, **kwargs):
        pem = self.pemeliharaan
        super().delete(*args, **kwargs)
        pem.hitung_total()

class KonsumsiBensin(models.Model):
    kendaraan = models.ForeignKey(
        Kendaraan, on_delete=models.PROTECT, verbose_name='Kendaraan'
    )
    tanggal = models.DateField('Tanggal Pengisian')
    km_pengisian = models.PositiveIntegerField('KM Saat Pengisian', blank=True, null=True)
    liter = models.DecimalField('Jumlah Liter', max_digits=6, decimal_places=2)
    harga_per_liter = models.DecimalField('Harga per Liter', max_digits=12, decimal_places=2)
    total_biaya = models.DecimalField('Total Biaya', max_digits=14, decimal_places=2, default=0)
    spbu = models.CharField('Nama SPBU', max_length=200, blank=True, default='')
    keterangan = models.TextField('Keterangan', blank=True, default='')
    tanggal_input = models.DateTimeField('Tanggal Input', auto_now_add=True)

    class Meta:
        app_label = 'pemeliharaan'
        ordering = ['-tanggal']
        verbose_name = 'Konsumsi Bensin'
        verbose_name_plural = 'Data Konsumsi Bensin'

    def __str__(self):
        return f"Bensin {self.kendaraan.nomor_polisi} - {self.tanggal.strftime('%d/%m/%Y')}"

    def save(self, *args, **kwargs):
        # Auto hitung total biaya
        self.total_biaya = self.liter * self.harga_per_liter
        super().save(*args, **kwargs)        