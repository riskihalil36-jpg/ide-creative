from flask import *
import sqlite3
import os
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "idecreative"

# =========================
# FOLDER CONFIG
# =========================
UPLOAD_FOLDER = "static/uploads"
INVOICE_FOLDER = "static/invoices"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(INVOICE_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["INVOICE_FOLDER"] = INVOICE_FOLDER

# =========================
# DATABASE
# =========================
def connect_db():
    conn = sqlite3.connect("booking.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = connect_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS bookings(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        telepon TEXT,
        tanggal TEXT,
        event TEXT,
        harga INTEGER,
        dp INTEGER,
        bukti TEXT,
        status TEXT

    )
    """)

    conn.commit()
    conn.close()


init_db()

# =========================
# HOME (SUDAH DIPERBAIKI + GALERI WEDDING)
# =========================
@app.route("/")
def home():

    return render_template_string("""
<!DOCTYPE html>
<html lang="id">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Ide Creative I.O</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{
    background:linear-gradient(135deg,#ffdce5,#fff7fa);
    font-family:'Segoe UI';
}

/* BOX UTAMA */
.box{
    width:90%;
    max-width:900px;
    margin:auto;
    margin-top:60px;
    background:white;
    border-radius:30px;
    padding:40px;
    text-align:center;
    box-shadow:0 15px 40px rgba(0,0,0,0.1);
}

/* TITLE */
.title{
    font-size:50px;
    font-weight:900;
    color:#ff3b7d;
}

/* SUB */
.sub{
    color:#666;
    margin-top:10px;
    font-size:18px;
}

/* BUTTON */
.btn-modern{
    display:block;
    margin-top:18px;
    padding:16px;
    border-radius:16px;
    text-decoration:none;
    color:white;
    font-size:18px;
    font-weight:bold;
}

.btn-book{
    background:linear-gradient(135deg,#2b7cff,#0066ff);
}

.btn-login{
    background:linear-gradient(135deg,#ff6ca8,#ff3b7d);
}

/* GALERI WEDDING */
.gallery{
    margin-top:40px;
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
    gap:15px;
}

.gallery img{
    width:100%;
    height:200px;
    object-fit:cover;
    border-radius:18px;
    box-shadow:0 10px 25px rgba(0,0,0,0.15);
}

</style>

</head>

<body>

<div class="box">

    <img src="/static/logo.png" width="110">

    <div class="title">
        Ide Creative I.O
    </div>

    <div class="sub">
        Solusi terbaik untuk semua acara kamu
    </div>

    <a href="/booking-page" class="btn-modern btn-book">
        Booking Event
    </a>

    <a href="/login-page" class="btn-modern btn-login">
        Login Admin
    </a>

    <!-- GALERI WEDDING -->
    <div class="gallery">

        <img src="/static/uploads/wedding1.jpg">
        <img src="/static/uploads/wedding2.jpg">
        <img src="/static/uploads/wedding3.jpg">
        <img src="/static/uploads/wedding4.jpg">

    </div>

</div>

</body>
</html>
""")

# =========================
# BOOKING PAGE
# =========================
@app.route("/booking-page")
def booking_page():

    return render_template_string("""

<!DOCTYPE html>
<html>
<head>

<title>Booking</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{
    background:linear-gradient(135deg,#ffdce5,#fff7fa);
    font-family:'Segoe UI';
}

.box{

    width:95%;
    max-width:650px;

    margin:auto;
    margin-top:40px;

    background:white;

    border-radius:30px;

    padding:40px;

    box-shadow:0 15px 40px rgba(0,0,0,0.1);
}

.title{

    text-align:center;

    font-size:40px;
    font-weight:900;

    color:#ff3b7d;

    margin-bottom:25px;
}

.form-control{

    padding:15px;

    border-radius:15px;

    margin-bottom:15px;
}

.btn-book{

    width:100%;

    background:linear-gradient(135deg,#ff6ca8,#ff3b7d);

    border:none;

    padding:15px;

    color:white;

    border-radius:15px;

    font-weight:bold;
}

.price-box{

    display:none;

    background:#fff0f5;

    border-radius:20px;

    padding:25px;

    margin-top:20px;
}

.qris img{
    width:220px;
}
 .booking-menu{

    display:flex;
    gap:15px;
    margin-bottom:25px;
    flex-wrap:wrap;
}

.booking-menu a{

    text-decoration:none;
    color:white;
    padding:14px 24px;
    border-radius:15px;
    font-weight:bold;
}

.menu-book{

    background:linear-gradient(
        135deg,
        #2b7cff,
        #005eff
    );
}

.menu-pengurus{

    background:linear-gradient(
        135deg,
        #ff6ca8,
        #ff3b7d
    );
}

.menu-portfolio{

    background:linear-gradient(
        135deg,
        #9c27b0,
        #673ab7
    );
}
</style>

</head>

<body>

<div class="box">
                                  
     <div class="booking-menu">

    <a href="/booking-page" class="menu-book">
        📝 Booking Event
    </a>

    <a href="/pengurus-public" class="menu-pengurus">
        👥 Struktur Pengurus
    </a>


</div>                             

    <a href="/" class="btn btn-dark mb-4">
        ← Dashboard
    </a>

    <div class="title">
        Booking Event
    </div>

    <form method="POST" action="/booking" enctype="multipart/form-data">

        <input type="text" name="nama" placeholder="Nama Lengkap" class="form-control" required>

        <input type="text" name="telepon" placeholder="Nomor WhatsApp" class="form-control" required>

        <input type="date" name="tanggal" class="form-control" required>

        <select name="event" id="event" class="form-control" onchange="updateHarga()" required>

            <option value="">
                Pilih Event
            </option>

            <option value="Wedding Organizer|15000000">
                Wedding Organizer
            </option>

            <option value="Birthday Party|5000000">
                Birthday Party
            </option>

            <option value="Seminar|8000000">
                Seminar
            </option>

            <option value="Concert|25000000">
                Music Concert
            </option>

        </select>

        <div id="priceBox" class="price-box">

            <h4>
                Harga : Rp <span id="hargaText"></span>
            </h4>

            <h3 style="color:#ff0066;">
                DP 50% : Rp <span id="dpText"></span>
            </h3>

            <div class="mt-4">

                <h4>Transfer:</h4>

                <h3>BCA - 1234567890</h3>

                <div>a/n Ide Creative</div>

            </div>

            <div class="qris text-center mt-4">

                <img src="/static/qris.png">

            </div>

            <div class="mt-4">

                <label>Upload Bukti Pembayaran</label>

                <input type="file" name="bukti" class="form-control" required>

            </div>

        </div>

        <input type="hidden" name="harga" id="hargaInput">
        <input type="hidden" name="dp" id="dpInput">

        <button class="btn-book">
            Booking Sekarang
        </button>

    </form>

</div>

<script>

function updateHarga(){

    let event = document.getElementById("event").value;

    if(event == ""){

        document.getElementById("priceBox").style.display = "none";
        return;
    }

    let data = event.split("|");

    let harga = parseInt(data[1]);

    let dp = harga / 2;

    document.getElementById("priceBox").style.display = "block";

    document.getElementById("hargaText").innerHTML =
    harga.toLocaleString("id-ID");

    document.getElementById("dpText").innerHTML =
    dp.toLocaleString("id-ID");

    document.getElementById("hargaInput").value = harga;

    document.getElementById("dpInput").value = dp;
}

</script>

</body>
</html>

""")


# =========================
# BOOKING
# =========================
@app.route("/booking", methods=["POST"])
def booking():

    nama = request.form["nama"]
    telepon = request.form["telepon"]
    tanggal = request.form["tanggal"]

    eventData = request.form["event"]

    harga = request.form["harga"]
    dp = request.form["dp"]

    event = eventData.split("|")[0]

    # =========================
    # UPLOAD FILE
    # =========================
    file = request.files.get("bukti")

    if not file or file.filename == "":

        return """

        <script>

        alert("Upload bukti pembayaran terlebih dahulu!");

        window.location.href='/booking-page';

        </script>

        """

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    # =========================
    # SAVE DATABASE
    # =========================
    conn = connect_db()
    c = conn.cursor()

    c.execute("""

    INSERT INTO bookings(

        nama,
        telepon,
        tanggal,
        event,
        harga,
        dp,
        bukti,
        status

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        nama,
        telepon,
        tanggal,
        event,
        harga,
        dp,
        filename,
        "Menunggu Konfirmasi"

    ))

    conn.commit()
    conn.close()

    # =========================
    # PDF INVOICE
    # =========================
    invoice_name = f"invoice_{nama}.pdf"

    pdf_path = os.path.join(
        app.config["INVOICE_FOLDER"],
        invoice_name
    )

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "<font size=24 color='hotpink'><b>INVOICE IDE CREATIVE</b></font>",
        styles['Title']
    )

    elements.append(title)
    elements.append(Spacer(1,20))

    data_invoice = [

        ["Nama", nama],
        ["Telepon", telepon],
        ["Tanggal Event", tanggal],
        ["Event", event],
        ["Harga", f"Rp {int(harga):,}"],
        ["DP 50%", f"Rp {int(float(dp)):,}"],
        ["Status", "Menunggu Konfirmasi"]

    ]

    table = Table(
        data_invoice,
        colWidths=[180,300]
    )

    table.setStyle(TableStyle([

        ('GRID',(0,0),(-1,-1),1,colors.black),

        ('BACKGROUND',(0,0),(0,-1),colors.pink),

        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),

        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),

        ('BOTTOMPADDING',(0,0),(-1,-1),12)

    ]))

    elements.append(table)

    thanks = Paragraph(

    "<font size=14 color='hotpink'><b>Terima kasih telah booking di Ide Creative 💖</b></font>",

    styles['Normal']

    )

    elements.append(Spacer(1,25))
    elements.append(thanks)

    doc.build(elements)

    # =========================
    # WHATSAPP AUTO
    # =========================
    wa = f"https://wa.me/6281342527108?text=🔥 BOOKING BARU IDE CREATIVE %0A%0A👤 Nama : {nama}%0A📞 Telepon : {telepon}%0A📅 Tanggal : {tanggal}%0A🎉 Event : {event}%0A💰 Harga : Rp {harga}%0A🔥 DP : Rp {dp}%0A%0A✅ Bukti pembayaran sudah diupload"

    # =========================
    # SUCCESS
    # =========================
    return f"""

    <script>

    alert("Booking berhasil! WhatsApp akan dibuka.");

    // buka invoice PDF
    window.open('/static/invoices/{invoice_name}', '_blank');

    // redirect ke WhatsApp
    setTimeout(function(){{
        window.location.href = "{wa}";
    }}, 1000);

    </script>

    """


# =========================
# LOGIN PAGE
# =========================

# =========================
# PENGURUS PUBLIC
# =========================
@app.route("/pengurus-public")
def pengurus_public():

    return """

<!DOCTYPE html>
<html>
<head>

<title>Struktur Pengurus Ide Creative</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{
    background:linear-gradient(135deg,#ffdce5,#fff7fa);
    font-family:'Segoe UI';
}

.container-box{
    width:95%;
    max-width:1200px;
    margin:auto;
    margin-top:40px;
    background:white;
    padding:30px;
    border-radius:30px;
}

.title{
    text-align:center;
    font-size:40px;
    font-weight:900;
    color:#ff3b7d;
    margin-bottom:30px;
}

.card-box{
    background:#fff5f8;
    border-radius:20px;
    padding:20px;
    text-align:center;
}

.card-box img{
    width:150px;
    height:150px;
    object-fit:cover;
    border-radius:50%;
    margin-bottom:15px;
}

.nav-btn{
    text-decoration:none;
    color:white;
    padding:12px 20px;
    border-radius:15px;
    margin-right:10px;
}

.back-btn{
    background:#222;
}

.portfolio-btn{
    background:#ff3b7d;
}

</style>

</head>

<body>

<div class="container-box">

    <a href="/booking-page" class="nav-btn back-btn">
        ← Booking Event
    </a>


    <div class="title">
        Struktur Pengurus Ide Creative
    </div>

    <div class="row">

        <div class="col-md-4 mb-4">
            <div class="card-box">
                <img src="/static/pengurus/ceo.jpg">
                <h4>Rizki Halil</h4>
                <p>CEO & Founder</p>
            </div>
        </div>

        <div class="col-md-4 mb-4">
            <div class="card-box">
                <img src="/static/pengurus/manager.jpg">
                <h4>Andi Saputra</h4>
                <p>Manager Event</p>
            </div>
        </div>

        <div class="col-md-4 mb-4">
            <div class="card-box">
                <img src="/static/pengurus/admin.jpg">
                <h4>Siti Rahma</h4>
                <p>Admin Keuangan</p>
            </div>
        </div>

    </div>

    <hr>

    <div id="portfolio">

        <h2 style="color:#ff3b7d;">
            📁 Portfolio Ide Creative
        </h2>

        <embed
        src="/static/portfolio/IdeCreative.pdf"
        type="application/pdf"
        width="100%"
        height="900px">

    </div>

</div>

</body>
</html>

"""

@app.route("/login-page")
def login_page():

    return render_template_string("""

<!DOCTYPE html>
<html>
<head>

<title>Login Admin</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"/>

<style>

body{

    background:
    linear-gradient(
    135deg,
    #ffdce5,
    #fff7fa
    );

    font-family:'Segoe UI';
}

/* LOGIN BOX */

.login-box{

    width:95%;
    max-width:520px;

    margin:auto;
    margin-top:40px;

    background:white;

    padding:40px;

    border-radius:30px;

    box-shadow:
    0 15px 40px rgba(255,105,180,0.15);
}

/* TITLE */

.title{

    text-align:center;

    font-size:42px;
    font-weight:900;

    color:#ff4d8d;

    margin-bottom:20px;
}

/* BIODATA */

.bio-box{

    background:#fff0f5;

    border:2px solid #ffd6e7;

    border-radius:25px;

    padding:25px;

    margin-bottom:30px;

    text-align:center;
}

.bio-logo{

    width:100px;

    margin-bottom:15px;
}

.bio-title{

    font-size:30px;

    font-weight:900;

    color:#ff3b7d;
}

.bio-sub{

    color:#666;

    margin-top:10px;

    line-height:1.8;
}

.bio-info{

    margin-top:20px;

    text-align:left;
}

.bio-item{

    margin-bottom:15px;

    color:#444;

    font-size:16px;

    line-height:1.8;
}

.bio-item i{

    color:#ff3b7d;

    width:30px;
}

/* FORM */

.form-control{

    padding:15px;

    border-radius:15px;

    margin-bottom:18px;

    border:1px solid #ffc2d6;
}

.form-control:focus{

    box-shadow:none;

    border-color:#ff4d8d;
}

/* BUTTON */

.btn-login{

    width:100%;

    background:
    linear-gradient(
    135deg,
    #ff6ca8,
    #ff3b7d
    );

    border:none;

    padding:15px;

    color:white;

    border-radius:15px;

    font-size:18px;
    font-weight:bold;

    transition:0.3s;
}

.btn-login:hover{

    transform:translateY(-2px);

    opacity:0.9;
}

/* BACK BUTTON */

.btn-back{

    display:inline-block;

    margin-bottom:20px;

    text-decoration:none;

    color:white;

    background:#111;

    padding:10px 18px;

    border-radius:12px;

    font-weight:bold;
}

/* FOOTER */

.footer{

    text-align:center;

    margin-top:20px;

    color:#777;

    font-size:14px;
}

</style>

</head>

<body>

<div class="login-box">

    <!-- BACK -->
    <a href="/" class="btn-back">
        ← Dashboard
    </a>

    <!-- TITLE -->
    <div class="title">
        Login Admin
    </div>

    <!-- LOGIN FORM -->
    <form method="POST" action="/login">

        <input
        type="text"
        name="username"
        placeholder="Username"
        class="form-control"
        required>

        <input
        type="password"
        name="password"
        placeholder="Password"
        class="form-control"
        required>

        <button class="btn-login">

            <i class="fa-solid fa-lock"></i>

            Login Sekarang

        </button>

    </form>
                                  
                                  

    <!-- FOOTER -->
    <div class="footer">

        © 2026 Ide Creative I.O<br>

        All rights reserved

    </div>

</div>

</body>
</html>

""")

# =========================
# STRUKTUR PENGURUS + PORTFOLIO
# =========================
@app.route("/pengurus")
def pengurus():

    if not session.get("admin"):
        return redirect("/")

    return """

<!DOCTYPE html>
<html>
<head>

<title>Struktur Pengurus</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{

    background:linear-gradient(135deg,#ffdce5,#fff7fa);

    font-family:'Segoe UI';
}

/* BOX */

.box{

    width:95%;
    max-width:1400px;

    margin:auto;
    margin-top:40px;

    background:white;

    border-radius:30px;

    padding:35px;

    box-shadow:0 15px 40px rgba(255,105,180,0.15);
}

/* TITLE */

.title{

    text-align:center;

    font-size:50px;
    font-weight:900;

    color:#ff3b7d;

    margin-bottom:30px;
}

/* BUTTON */

.btn-back{

    background:black;

    color:white;

    padding:12px 20px;

    border-radius:12px;

    text-decoration:none;

    font-weight:bold;
}

/* NAV */

.nav-tabs .nav-link{

    color:#ff3b7d;

    font-weight:bold;
}

/* CARD */

.card-box{

    background:#fff7fa;

    border-radius:25px;

    padding:25px;

    height:100%;
}

.foto{

    width:150px;
    height:150px;

    object-fit:cover;

    border-radius:50%;

    display:block;

    margin:auto;

    border:5px solid pink;
}

.nama{

    text-align:center;

    margin-top:20px;

    font-size:28px;
    font-weight:900;

    color:#ff3b7d;
}

.jabatan{

    text-align:center;

    color:#666;

    margin-bottom:20px;
}

.bio{

    line-height:2;
}

/* PDF */

.pdf{

    width:100%;

    height:850px;

    border:none;

    margin-top:20px;

    border-radius:20px;
}

</style>

</head>

<body>

<div class="box">

    <a href="/admin" class="btn-back">

        ← Dashboard

    </a>

    <div class="title">

        Ide Creative

    </div>

    <!-- TAB -->
    <ul class="nav nav-tabs mb-4" id="myTab">

        <li class="nav-item">

            <button
            class="nav-link active"
            data-bs-toggle="tab"
            data-bs-target="#pengurus">

            👥 Struktur Pengurus

            </button>

        </li>

        <li class="nav-item">

            <button
            class="nav-link"
            data-bs-toggle="tab"
            data-bs-target="#portfolio">

            📁 Portfolio

            </button>

        </li>

    </ul>

    <!-- TAB CONTENT -->
    <div class="tab-content">

        <!-- PENGURUS -->
        <div class="tab-pane fade show active" id="pengurus">

            <div class="row g-4">

                <!-- CEO -->
                <div class="col-md-4">

                    <div class="card-box">

                        <img
                        src="/static/pengurus/ceo.jpg"
                        class="foto">

                        <div class="nama">

                            Rizki Halil

                        </div>

                        <div class="jabatan">

                            CEO / Founder

                        </div>

                        <div class="bio">

                            👤 Umur : 21 Tahun<br>

                            📍 Indonesia<br>

                            📞 0813-4252-7108<br>

                            💼 Mengatur seluruh perusahaan

                        </div>

                    </div>

                </div>

                <!-- MANAGER -->
                <div class="col-md-4">

                    <div class="card-box">

                        <img
                        src="/static/pengurus/manager.jpg"
                        class="foto">

                        <div class="nama">

                            Andi Saputra

                        </div>

                        <div class="jabatan">

                            Manager Event

                        </div>

                        <div class="bio">

                            👤 Umur : 24 Tahun<br>

                            📍 Jakarta<br>

                            💼 Mengatur jalannya event

                        </div>

                    </div>

                </div>

                <!-- ADMIN -->
                <div class="col-md-4">

                    <div class="card-box">

                        <img
                        src="/static/pengurus/admin.jpg"
                        class="foto">

                        <div class="nama">

                            Siti Rahma

                        </div>

                        <div class="jabatan">

                            Admin Keuangan

                        </div>

                        <div class="bio">

                            👤 Umur : 23 Tahun<br>

                            📍 Bandung<br>

                            💼 Mengatur laporan keuangan

                        </div>

                    </div>

                </div>

            </div>

        </div>

        <!-- PORTFOLIO -->
        <div class="tab-pane fade" id="portfolio">

            <h2 style="color:#ff3b7d;">

                Portfolio Ide Creative

            </h2>

            <object
            data="/static/portfolio/IdeCreative.pdf"
            type="application/pdf"
            class="pdf">

            </object>

        </div>

    </div>

</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>

"""

# ==========================
# LOGIN PROCESS
# =========================
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    if username == "idecreative" and password == "ide123":

        session["admin"] = True

        return redirect(url_for("admin"))

    return """

    <center style='margin-top:50px;'>

    <h1 style='color:red;'>Login Gagal</h1>

    <a href='/login-page'>Coba Lagi</a>

    </center>

    """


# =========================
# ADMIN
# =========================
@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/")

    conn = connect_db()
    c = conn.cursor()

    c.execute("""
    SELECT * FROM bookings
    ORDER BY id DESC
    """)

    data = c.fetchall()
    conn.close()

    total = len(data)

    pending = len([
        x for x in data
        if x["status"] == "Menunggu Konfirmasi"
    ])

    confirmed = len([
        x for x in data
        if x["status"] == "Confirmed"
    ])

    rejected = len([
        x for x in data
        if x["status"] == "Rejected"
    ])

    return render_template_string("""

<!DOCTYPE html>

<html>
<head>

<title>Dashboard Booking</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{
    background:linear-gradient(135deg,#ffdce5,#fff7fa);
    font-family:'Segoe UI';
}

.box{
    width:95%;
    margin:auto;
    margin-top:40px;
    background:white;
    border-radius:30px;
    padding:30px;
    box-shadow:0 15px 40px rgba(0,0,0,0.1);
}

img{
    width:120px;
    border-radius:15px;
}

.admin-navbar{
    display:flex;
    gap:15px;
    margin-bottom:25px;
    flex-wrap:wrap;
}

.nav-btn{
    text-decoration:none;
    color:white;
    padding:14px 24px;
    border-radius:15px;
    font-weight:bold;
}

.booking-btn{
    background:linear-gradient(135deg,#2b7cff,#005eff);
}

.pengurus-btn{
    background:linear-gradient(135deg,#ff6ca8,#ff3b7d);
}

.logout-btn{
    background:linear-gradient(135deg,#444,#111);
}

</style>

</head>

<body>

<div class="box">

<div class="admin-navbar">


<a href="/pengurus" class="nav-btn pengurus-btn">
    👥 Struktur Pengurus + Portfolio
</a>

<a href="/logout" class="nav-btn logout-btn">
    🚪 Logout
</a>

</div>

<div class="row mb-4">

<div class="col-md-3">
    <div class="card text-center shadow">
        <div class="card-body">
            <h5>Total Booking</h5>
            <h2>{{total}}</h2>
        </div>
    </div>
</div>

<div class="col-md-3">
    <div class="card text-center shadow">
        <div class="card-body">
            <h5>Pending</h5>
            <h2>{{pending}}</h2>
        </div>
    </div>
</div>

<div class="col-md-3">
    <div class="card text-center shadow">
        <div class="card-body">
            <h5>Confirmed</h5>
            <h2>{{confirmed}}</h2>
        </div>
    </div>
</div>

<div class="col-md-3">
    <div class="card text-center shadow">
        <div class="card-body">
            <h5>Rejected</h5>
            <h2>{{rejected}}</h2>
        </div>
    </div>
</div>

</div>

<div class="table-responsive">

<table class="table table-bordered">

<thead class="table-dark">

<tr>
<th>ID</th>
<th>Nama</th>
<th>Telepon</th>
<th>Event</th>
<th>Harga</th>
<th>DP</th>
<th>Bukti</th>
<th>Status</th>
<th>Aksi</th>
</tr>

</thead>

<tbody>

{% for d in data %}

<tr>

<td>{{d.id}}</td>
<td>{{d.nama}}</td>
<td>{{d.telepon}}</td>
<td>{{d.event}}</td>

<td>Rp {{ "{:,}".format(d.harga|int) }}</td>

<td>Rp {{ "{:,}".format(d.dp|int) }}</td>

<td>

{% if d.bukti %}

<a href="/static/uploads/{{d.bukti}}" target="_blank">
<img src="/static/uploads/{{d.bukti}}">
</a>

{% else %}
Tidak ada bukti
{% endif %}

</td>

<td>{{d.status}}</td>

<td>

<a href="/update/{{d.id}}/Confirmed"
class="btn btn-success btn-sm">
Confirm </a>

<a href="/update/{{d.id}}/Rejected"
class="btn btn-danger btn-sm">
Reject </a>

</td>

</tr>

{% endfor %}

</tbody>

</table>

</div>

</div>

</body>
</html>

""",
data=data,
total=total,
pending=pending,
confirmed=confirmed,
rejected=rejected
)

                                  
# =========================
# UPDATE STATUS
# =========================
@app.route("/update/<int:id>/<status>")
def update(id, status):

    if not session.get("admin"):
        return redirect("/")

    conn = connect_db()
    c = conn.cursor()

    c.execute("""

    UPDATE bookings
    SET status=?

    WHERE id=?

    """, (status, id))

    conn.commit()
    conn.close()

    return redirect("/admin")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================
# ERROR HANDLER
# =========================
@app.errorhandler(404)
def not_found(e):

    return """

    <h1 style='text-align:center;margin-top:50px;'>

    404 Halaman Tidak Ditemukan

    </h1>

    """


@app.errorhandler(500)
def server_error(e):

    return """

    <h1 style='text-align:center;color:red;margin-top:50px;'>

    500 Internal Server Error

    </h1>

    """

# =========================
# RUN APP
# =========================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)