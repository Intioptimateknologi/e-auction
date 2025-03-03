from . import models
from mfa import models as mfa_models
from drf_extra_fields.fields import Base64FileField
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
import PyPDF2
import io
import base64
import math, random

# class PDFBase64File(Base64FileField):
#     ALLOWED_TYPES = ['pdf']

#     def get_file_extension(self, filename, decoded_file):
#         try:
#             if base64.b64encode(decoded_file).decode('ascii')[0:4] != 'http':
#                 PyPDF2.PdfFileReader(io.BytesIO(decoded_file))
#         except PyPDF2.utils.PdfReadError as e:
#             print(e)
#         else:
#             return 'pdf'

class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        return 'pdf'

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)

class dokumen_perusahaanSerializer(serializers.ModelSerializer):
    dokumen = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = models.dokumen_perusahaan
        fields = [
            "dokumen",
            "nama_dokumen",
            "verification_note",
            "last_updated",
            "verified_at",
            "created",
            "verified",
            "verified_by",
            "id_perusahaan"
        ]
        # dokumen = PDFBase64File(required=False)
    

class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class CostumGroupSerializer(serializers.HyperlinkedModelSerializer):
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    diubah_oleh = serializers.ReadOnlyField(source="diubah_oleh.nama_lengkap")
    class Meta:
        model = models.CustomGroup
        fields = ['id','keterangan',"name","active","last_updated","dibuat_oleh","diubah_oleh"]

class UsersViewSerializer(serializers.ModelSerializer):
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    diubah_oleh = serializers.ReadOnlyField(source="diubah_oleh.nama_lengkap")
    customGroup = CostumGroupSerializer(many=True)
   # user_type = ChoiceField(choices=models.Users.UserType.choices)
    class Meta:
        model = models.Users
        fields = [
            "id",
            "isactive",
            "is_active",
            "email",
            "created",
            "username",
            "last_updated",
            "dibuat_oleh",
            "diubah_oleh",
            "password",
            "mobile_number",
            "customGroup",
            "nama_lengkap",
            "user_type",
            "masaberlaku1",
            "masaberlaku2",
            "password_terlihat",
        ]

class UsersSerializer(serializers.ModelSerializer):
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    diubah_oleh = serializers.ReadOnlyField(source="diubah_oleh.nama_lengkap")
    #pending = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Users
        fields = [
            "id",
            "isactive",
            "is_active",
            "email",
            "created",
            "username",
            "password",
            "mobile_number",
            "customGroup",
            "nama_lengkap",
            "user_type",
            "masaberlaku1",
            "masaberlaku2",
            "password_terlihat",
            "pending",
            "dibuat_oleh",
            "diubah_oleh",
            "created",
            "last_updated",
            "last_login",
            "first_login"
        ]
    def get_pending(self, obj):
        return obj.last_login == None
    
    def create(self, validated_data):
        corpus= "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        size = 10
        generate_OTP = ""
        length = len(corpus)
        for i in range(size) :
            generate_OTP+= corpus[math.floor(random.random() * length)]
        print(generate_OTP)
        user = super(UsersSerializer, self).create(validated_data)
        user.set_password(generate_OTP)
        user.password_terlihat=generate_OTP
        user.save()
        return user

class tim_lelangSerializer(serializers.ModelSerializer):
    #users_set = UsersSerializer(many=False, read_only=False)
    username = serializers.ReadOnlyField(source='users.username')
    nama_lengkap = serializers.ReadOnlyField(source='users.nama_lengkap')
    sk_pengangkatan = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    diubah_oleh = serializers.ReadOnlyField(source="diubah_oleh.nama_lengkap")
    class Meta:
        model = models.tim_lelang
        fields = [
            "id",
            "users",
            "username",
            "nama_lengkap",
            "nip",
            "jabatan",
            "jabatan_dalam_tim",
            "sk_pengangkatan",
            "active",
            "dibuat_oleh",
            "diubah_oleh",
            "created",
            "last_updated",
        ]

        #depth = 1

class adminSerializer(serializers.ModelSerializer):
    nama_lengkap = serializers.ReadOnlyField(source='users.nama_lengkap')
    username = serializers.ReadOnlyField(source='users.username')
    is_active = serializers.ReadOnlyField(source='users.is_active')
    sk_pengangkatan = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    diubah_oleh = serializers.ReadOnlyField(source="diubah_oleh.nama_lengkap")
    class Meta:
        model = models.admin
        fields = [
            "id",
            "nip",
            "sk_pengangkatan",
            "jabatan_dalam_tim",
            "jabatan",
            "active",
            "dibuat_oleh",
            "diubah_oleh",
            "created",
            "last_updated",
            "users",
            "username",
            "nama_lengkap",
            "is_active",
        ]
        #depth = 1

class viewerSerializer(serializers.ModelSerializer):
    nama_lengkap = serializers.ReadOnlyField(source='users.nama_lengkap')
    username = serializers.ReadOnlyField(source='users.username')
    sk_pengangkatan = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    diubah_oleh = serializers.ReadOnlyField(source="diubah_oleh.nama_lengkap")
    class Meta:
        model = models.viewers
        fields = [
            "id",
            "nip",
            "sk_pengangkatan",
            "jabatan_dalam_tim",
            "jabatan",
            "username",
            "nama_lengkap",
            "users",
            "dibuat_oleh",
            "diubah_oleh",
            "created",
            "last_updated",
        ]

class bidderlistSerializer(serializers.ModelSerializer):
    #users_set = UsersSerializer(many=False, read_only=False)
    # sk_pengangkatan = PDFBase64File(required=False)
    class Meta:
        model = models.bidder_list
        fields = [
            "id",
            "nip",
            "jabatan_dalam_tim",
            "jabatan",
            "users",
            "active",
        ]




class bidderSerializer(serializers.ModelSerializer):
    diubah_oleh = serializers.SerializerMethodField()
    dibuat_oleh = serializers.SerializerMethodField()
    # diubah_oleh = serializers.ReadOnlyField(source="diubah_oleh.nama_lengkap")
    # dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    class Meta:
        model = models.bidder
        fields = [
            "id",
            "active",
            "alamat_perusahaan",
            "jenis_penyelenggara",
            "verified",
            "verified_at",
            "telp_perusahaan",
            "nama_perusahaan",
            "verification_note",
            "npwp_perusahaan",
            "email_perusahaan",
            "nib_perusahaan",
            "verified_by",
            "surat_kuasa",
            "dibuat_oleh",
            "diubah_oleh",
            "created",
            "last_updated",
        ]
    
    def get_diubah_oleh(self, obj):
        if obj.diubah_oleh:
            return {"id": obj.diubah_oleh.id, "nama_lengkap": obj.diubah_oleh.nama_lengkap}
        return None

    def get_dibuat_oleh(self, obj):
        if obj.dibuat_oleh:
            return {"id": obj.dibuat_oleh.id, "nama_lengkap": obj.dibuat_oleh.nama_lengkap}
        return None

class UserMenuSerializer(serializers.ModelSerializer):
    leaf_nodes = serializers.SerializerMethodField()

    class Meta:
        model = models.UserMenu
        fields = [
            "id",
            "parent",
            "name",
            "slug",
            "additional_text",
            "additional_text2",
            "additional_text3",
            "additional_text4",
            "icon_class",
            "style_class",
            "order",
            "enabled",
            "link",
            "leaf_nodes",
            "tahapan"
        ]
    def get_leaf_nodes(self, obj):
        return UserMenuSerializer(obj.get_children(), many=True).data

class UserMenu2Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserMenu
        fields = [
            "id",
            "parent",
            "name",
            "slug",
            "additional_text",
            "additional_text2",
            "additional_text3",
            "additional_text4",
            "icon_class",
            "style_class",
            "order",
            "enabled",
            "link",
            "tahapan"
        ]

class UserMenuGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserMenuGroup
        fields = [
            "menu","group"
        ]

# dibuat untuk menggantikan BidderUserSerializer sebagai crud
class BidderUser2Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.bidder_user
        fields = [
            "id",
            "users",
            "bidder",
            "active",
        ]

class BidderUserSerializer(serializers.ModelSerializer):
    nama_perusahaan = serializers.ReadOnlyField(source='bidder.nama_perusahaan')
    nama_user = serializers.ReadOnlyField(source='users.nama_lengkap')
    username = serializers.ReadOnlyField(source='users.username')
    email = serializers.ReadOnlyField(source='users.email')
    users = UsersSerializer(read_only = True)
    bidder = bidderSerializer(read_only = True)
    diubah_oleh = serializers.SerializerMethodField()
    dibuat_oleh = serializers.SerializerMethodField()
    
    # dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    # diubah_oleh = serializers.ReadOnlyField(source="diubah_oleh.nama_lengkap")
    
    class Meta:
        model = models.bidder_user
        fields = [
            "id",
            "users",
            "bidder",
            "nama_perusahaan",
            "email",
            "username",
            "nama_user",
            "active",
            "dibuat_oleh",
            "diubah_oleh",
            "created",
            "last_updated",
        ]
        
    def get_diubah_oleh(self, obj):
        if obj.diubah_oleh:
            return {"id": obj.diubah_oleh.id, "nama_lengkap": obj.diubah_oleh.nama_lengkap}
        return None

    def get_dibuat_oleh(self, obj):
        if obj.dibuat_oleh:
            return {"id": obj.dibuat_oleh.id, "nama_lengkap": obj.dibuat_oleh.nama_lengkap}
        return None

class bidderperwakilanSerializer(serializers.ModelSerializer):
    sk_pengangkatan = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    
    ttd = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    nama_perusahaan = serializers.ReadOnlyField(source='bidder.bidder.nama_perusahaan')
    akun = serializers.ReadOnlyField(source='bidder.users.username')
    
    
    dibuat_oleh = serializers.SerializerMethodField()
    diubah_oleh = serializers.SerializerMethodField()
    # dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    # diubah_oleh = serializers.ReadOnlyField(source="diubah_oleh.nama_lengkap")
    
    
    bidder = BidderUserSerializer(read_only = True)
    class Meta:
        model = models.bidder_perwakilan
        fields = [
            "id",
            "nama_lengkap",
            "nik_perwakilan",
            "akun",
            "email",
            "mobile_number",
            "jabatan",
            "ip_address",
            "active",
            "sk_pengangkatan",
            "ttd",
            "nama_perusahaan",
            "bidder",
            "profil_peruri",
            "dibuat_oleh",
            "diubah_oleh",
            "created",
            "last_updated",
        ]
        
    def get_diubah_oleh(self, obj):
        if obj.diubah_oleh:
            return {"id": obj.diubah_oleh.id, "nama_lengkap": obj.diubah_oleh.nama_lengkap}
        return None

    def get_dibuat_oleh(self, obj):
        if obj.dibuat_oleh:
            return {"id": obj.dibuat_oleh.id, "nama_lengkap": obj.dibuat_oleh.nama_lengkap}
        return None

# Dibuat untuk menggantikan bidderperwakilanserializer
class crudbidderperwakilanserializer(serializers.ModelSerializer):
    class Meta:
        model = models.bidder_perwakilan
        fields = [
            "id",
            "nama_lengkap",
            "nik_perwakilan",
            "email",
            "mobile_number",
            "jabatan",
            "ip_address",
            "active",
            "sk_pengangkatan",
            "ttd",
            "bidder",
            "profil_peruri",
            "dibuat_oleh",
            "diubah_oleh",
            "created",
            "last_updated",
        ]

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Group
        fields = ['id','name','url']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id','nama_lengkap','username', 'email', 'groups', 'url', ]

class GroupMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.menugroup_map
        fields = [
            'id',
            "group",
            "name",
            "menuid",
            "parent_id"
        ]
        
class MFAKeyMonitoringSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = mfa_models.MFAKey
        fields = "__all__"
        
    def get_user(self, obj):
        return {"id": obj.user.id, "username": obj.user.username}

class NotifikasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notifikasi
        fields = "__all__"