from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt #, csrf_protect, requires_csrf_token
import json
from django.http import QueryDict

def formatResult(rows):
    result = []
    for row in rows:
        row = {
            'id': row[0],
            'nama': row[1],
            'jenis_kelamin': row[2],
            'keturunan_ke': row[3],
            'keturunan_dari_id': row[4],
        }
        result.append(row)

    return result

# Create your views here.
def index(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT nama FROM Budi WHERE keturunan_ke = 1")
        rows = cursor.fetchall()

        result = rows
 
    return JsonResponse(
        {
            'result': result 
        }
    )

def cucuBudi(request):
    jenis_kelamin = request.GET.get('jenis_kelamin','')
    print(jenis_kelamin)
    with connection.cursor() as cursor:
        try:
            if not jenis_kelamin:
                cursor.execute("SELECT nama FROM Budi WHERE keturunan_ke >= 2")
            else:
                cursor.execute(f"SELECT nama FROM Budi WHERE keturunan_ke >= 2 AND jenis_kelamin = '{jenis_kelamin}'")
            rows = cursor.fetchall()
            result = rows
        except Exception as e:
            result = 'error'

        return JsonResponse(
            {
                'result': result
            }
        )

def bibiDari(request, nama):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT keturunan_ke FROM budi WHERE nama = '{nama}' COLLATE NOCASE") # COLLATE NOCASE untuk menghihndari case sensitive pada sqlite
        keturunan_ke = cursor.fetchone()

        cursor.execute(f"SELECT nama FROM budi WHERE keturunan_ke < {keturunan_ke[0]} AND jenis_kelamin = 'wanita'")
        bibi = cursor.fetchall()

        result = bibi
 
    return JsonResponse(
        {'result': result}
    )

def pamanDari(request, nama):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT keturunan_ke FROM budi WHERE nama = '{nama}' COLLATE NOCASE") # COLLATE NOCASE untuk menghihndari case sensitive pada sqlite
        keturunan_ke = cursor.fetchone()

        cursor.execute(f"SELECT nama FROM budi WHERE keturunan_ke < {keturunan_ke[0]} AND jenis_kelamin = 'pria'")
        paman = cursor.fetchall()

        result = paman
 
    return JsonResponse(
        {'result': result}
    )

def sepupuDari(request, nama):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT keturunan_ke FROM budi WHERE nama = '{nama}' COLLATE NOCASE")
        keturunan_ke = cursor.fetchone()

        if request.GET.get('jenis_kelamin', ''):
            cursor.execute(f"SELECT nama FROM budi WHERE keturunan_ke = {keturunan_ke[0]} AND jenis_kelamin = '{request.GET.get('jenis_kelamin')}'")
        else:
            cursor.execute(f"SELECT nama FROM budi WHERE keturunan_ke = {keturunan_ke[0]}")
        sepupu = cursor.fetchall()

        result = sepupu
 
    return JsonResponse(
        {'result': result}
    )

@csrf_exempt
def orang(request, nama_or_id=None):
    def getBodyRequest(key=None, default=None):
        # get body request manually
        body_request = json.loads(request.body.decode('utf-8'))
        try:
            return body_request[key]
        except:
            return default

    if request.method == 'GET':
        with connection.cursor() as cursor:
            if nama_or_id:
                if nama_or_id.isdigit():
                    cursor.execute(f"SELECT * FROM budi WHERE id = '{nama_or_id}' COLLATE NOCASE")
                else:
                    cursor.execute(f"SELECT * FROM budi WHERE nama = '{nama_or_id}' COLLATE NOCASE")
            else:
                cursor.execute(f"SELECT * FROM budi")
            orang = cursor.fetchall()

            result = formatResult(orang)
            
            return JsonResponse(
                {'result': result}
            )
    
    if request.method == "POST":
        nama = getBodyRequest('nama')
        jenis_kelamin = getBodyRequest('jenis_kelamin')
        keturunan_dari_id = getBodyRequest('keturunan_dari_id', 0)

        genders = ['pria', 'wanita']
        if jenis_kelamin in genders:
            pass
        else:
            jenis_kelamin = 'pria'

        with connection.cursor() as cursor:
            if nama and jenis_kelamin: # required
                # dapatkan urutan keturunan
                cursor.execute(f"SELECT keturunan_ke FROM budi WHERE id = {keturunan_dari_id}")
                urutan_keturunan_orang_tua = cursor.fetchone()[0]
                keturunan_ke = urutan_keturunan_orang_tua+1

                message = "success"
                try:
                    cursor.execute(f"INSERT INTO budi (nama, jenis_kelamin, keturunan_ke, keturunan_dari_id) VALUES ('{nama}', '{jenis_kelamin}', {keturunan_ke}, {keturunan_dari_id})")
                except:
                    message = "failed"
            else:
                message = "failed"

            # reset auto increment
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'budi'")

        return JsonResponse(
            {
                "message": message
            }
        )
    if request.method == "PUT":
        id = getBodyRequest('id')
        nama = getBodyRequest('nama')
        jenis_kelamin = getBodyRequest('jenis_kelamin')

        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE budi SET nama = {nama},")

    if request.method == "DELETE":
        id = getBodyRequest('id')

        with connection.cursor() as cursor:
            try:
                # cek apakah mempunyai anak
                cursor.execute(f"SELECT id FROM budi WHERE keturunan_dari_id = {id} ")
                if cursor.fetchone() != None: 
                    # jika mempunyai anak
                    message = "failed"
                else:
                    # jjika tidak mempunyai anak
                    message = "success"
                    cursor.execute(f"DELETE FROM budi WHERE id={id}")
            except:
                message = "failed"

            # reset auto increment
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'budi'")

        return JsonResponse(
            {
                "message": message
            }
        )
@csrf_exempt
def test(request):

    return JsonResponse(
        {
            "result": request.method
        }
    )