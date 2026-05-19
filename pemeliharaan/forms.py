from django import forms

from .models import (
    Kendaraan, Bengkel, SparePart, JasaServis,
    Pemeliharaan, DetailSparePart, DetailJasaServis, KonsumsiBensin # TAMBAHKAN INI
)


class KendaraanForm(forms.ModelForm):
    class Meta:
        model = Kendaraan
        fields = ['jenis', 'nomor_polisi', 'merk', 'tipe', 'tahun_pembuatan',
                  'warna', 'no_rangka', 'no_mesin', 'pemilik_pengguna',
                  'foto', 'keterangan', 'aktif'] # Pastikan 'foto' ada di sini
        widgets = {
            'jenis': forms.Select(attrs={'class': 'form-select text-start'}),
            'nomor_polisi': forms.TextInput(attrs={'class': 'form-control text-start'}),
            'merk': forms.TextInput(attrs={'class': 'form-control text-start'}),
            'tipe': forms.TextInput(attrs={'class': 'form-control text-start'}),
            'tahun_pembuatan': forms.NumberInput(attrs={'class': 'form-control text-start'}),
            'warna': forms.TextInput(attrs={'class': 'form-control text-start'}),
            'no_rangka': forms.TextInput(attrs={'class': 'form-control text-start'}),
            'no_mesin': forms.TextInput(attrs={'class': 'form-control text-start'}),
            'pemilik_pengguna': forms.TextInput(attrs={'class': 'form-control text-start'}),
            # Widget untuk foto
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control text-start', 'accept': 'image/*'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control text-start', 'rows': 3}),
            'aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BengkelForm(forms.ModelForm):
    class Meta:
        model = Bengkel
        fields = ['nama_bengkel', 'pemilik', 'alamat', 'kota', 'no_telp',
                  'jenis_kendaraan', 'keterangan']
        widgets = {
            'nama_bengkel': forms.TextInput(attrs={'class': 'form-control'}),
            'pemilik': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'kota': forms.TextInput(attrs={'class': 'form-control'}),
            'no_telp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 021-1234567'}),
            'jenis_kendaraan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobil, Motor, Sepeda Listrik'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['kode', 'nama_sparepart', 'harga', 'keterangan']
        widgets = {
            'kode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: SP-001'}),
            'nama_sparepart': forms.TextInput(attrs={'class': 'form-control'}),
            'harga': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class JasaServisForm(forms.ModelForm):
    class Meta:
        model = JasaServis
        fields = ['kode', 'nama_jasa', 'biaya', 'keterangan']
        widgets = {
            'kode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: JS-001'}),
            'nama_jasa': forms.TextInput(attrs={'class': 'form-control'}),
            'biaya': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class PemeliharaanForm(forms.ModelForm):
    class Meta:
        model = Pemeliharaan
        fields = ['kendaraan', 'bengkel', 'tanggal_servis', 'km_saat_servis', 'keterangan']
        widgets = {
            'kendaraan': forms.Select(attrs={'class': 'form-select'}),
            'bengkel': forms.Select(attrs={'class': 'form-select'}),
            # Tambahkan format='%Y-%m-%d' agar <input type="date"> bisa membacanya
            'tanggal_servis': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'km_saat_servis': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    # Tambahkan __init__ agar format input dari server juga diterima dengan benar
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tanggal_servis'].input_formats = ['%Y-%m-%d']
        self.fields['kendaraan'].queryset = Kendaraan.objects.filter(aktif=True)
        

class DetailSparePartForm(forms.ModelForm):
    class Meta:
        model = DetailSparePart
        fields = ['sparepart', 'jumlah', 'harga_satuan']
        widgets = {
            'sparepart': forms.Select(attrs={'class': 'form-select', 'id': 'id_sparepart_select'}),
            'jumlah': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 1}),
            'harga_satuan': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'id': 'id_harga_satuan'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tambah data-harga ke setiap option
        self.fields['sparepart'].widget.choices = [('', '--- Pilih Spare Part ---')] + [
            (sp.pk, sp.nama_sparepart) for sp in SparePart.objects.all()
        ]
        


class DetailJasaServisForm(forms.ModelForm):
    class Meta:
        model = DetailJasaServis
        fields = ['jasa_servis', 'biaya']
        widgets = {
            'jasa_servis': forms.Select(attrs={'class': 'form-select', 'id': 'id_jasa_select'}),
            'biaya': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'id': 'id_biaya_jasa'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jasa_servis'].widget.choices = [('', '--- Pilih Jasa Servis ---')] + [
            (js.pk, js.nama_jasa) for js in JasaServis.objects.all()
        ]

class KonsumsiBensinForm(forms.ModelForm):
    class Meta:
        model = KonsumsiBensin
        fields = ['kendaraan', 'tanggal', 'km_pengisian', 'liter', 'harga_per_liter', 'spbu', 'keterangan']
        widgets = {
            'kendaraan': forms.Select(attrs={'class': 'form-select text-start'}),
            'tanggal': forms.DateInput(attrs={'class': 'form-control text-start', 'type': 'date'}, format='%Y-%m-%d'),
            'km_pengisian': forms.NumberInput(attrs={'class': 'form-control text-start', 'min': 0}),
            'liter': forms.NumberInput(attrs={'class': 'form-control text-start', 'min': 0, 'step': '0.01', 'id': 'id_liter_bensin'}),
            'harga_per_liter': forms.NumberInput(attrs={'class': 'form-control text-start', 'min': 0, 'id': 'id_harga_per_liter'}),
            'spbu': forms.TextInput(attrs={'class': 'form-control text-start', 'placeholder': 'Contoh: SPBU Pertamina Jl. Sudirman'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control text-start', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tanggal'].input_formats = ['%Y-%m-%d']
        self.fields['kendaraan'].queryset = Kendaraan.objects.filter(aktif=True)        