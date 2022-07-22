from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse, HttpResponseRedirect

def formatResult(rows):
    result = []
    for row in rows:
        row = {
            'id': row[0],
            'name': row[1],
            'jenis_kelamin': row[2],
            'keturunan_ke': row[3],
            'keturunan_dari': row[4],
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
            'data': result 
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
                'data': result
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
        {'data': result}
    )

def pamanDari(request, nama):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT keturunan_ke FROM budi WHERE nama = '{nama}' COLLATE NOCASE") # COLLATE NOCASE untuk menghihndari case sensitive pada sqlite
        keturunan_ke = cursor.fetchone()

        cursor.execute(f"SELECT nama FROM budi WHERE keturunan_ke < {keturunan_ke[0]} AND jenis_kelamin = 'pria'")
        paman = cursor.fetchall()

        result = paman
 
    return JsonResponse(
        {'data': result}
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
        {'data': result}
    )

def orang(request, nama=None):
    with connection.cursor() as cursor:
        if nama:
            cursor.execute(f"SELECT * FROM budi WHERE nama = '{nama}' COLLATE NOCASE")
        else:
            cursor.execute(f"SELECT * FROM budi")
        orang = cursor.fetchall()

        result = formatResult(orang)
 
    return JsonResponse(
        {'data': result}
    )