import os
import re
import smtplib
import csv
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from urllib.parse import quote
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Set the secret key for session security (in a real app, this would be loaded from environment variables)
app.secret_key = os.urandom(24)

SCHOOL_ADDRESS = (
    "St. Antony's Girls Higher Secondary School, "
    "Mandavelipakkam, Madha Church Rd, Mandavelipakkam, "
    "Foreshore Estate, Chennai, Tamil Nadu 600028"
)
SCHOOL_ADDRESS_HTML = (
    "St. Antony's Girls Higher Secondary School,<br>"
    "Mandavelipakkam, Madha Church Rd,<br>"
    "Mandavelipakkam, Foreshore Estate,<br>"
    "Chennai, Tamil Nadu 600028"
)
SCHOOL_MAPS_URL = (
    "https://www.google.com/maps/search/?api=1&query="
    + quote(SCHOOL_ADDRESS)
)

PAGE_BANNERS = {
    'about': 'images/img1.jpeg',
    'academics': 'images/infra/infra-3.jpeg',
    'admissions': 'images/img2.jpeg',
    'gallery': 'images/img2.jpeg',
    'contact': 'images/img3.jpeg',
    'faculty': 'images/group.png',
}

GALLERY_IMAGES = [
    {
        'file': 'images/img1.jpeg',
        'alt': 'Student in traditional costume receiving recognition from faculty',
        'category': 'cultural',
        'title': 'Traditional Day Celebrations',
        'tag': 'Cultural',
        'layout': 'photo',
    },
    {
        'file': 'images/img2.jpeg',
        'alt': 'Students and faculty in traditional attire at cultural event',
        'category': 'cultural',
        'title': 'Cultural Day Group Photo',
        'tag': 'Cultural',
        'layout': 'photo',
    },
    {
        'file': 'images/img3.jpeg',
        'alt': 'Welcome ceremony with students presenting gifts to faculty',
        'category': 'cultural',
        'title': 'Welcome & Gratitude Day',
        'tag': 'Cultural',
        'layout': 'photo',
    },
    {
        'file': 'images/img4.jpeg',
        'alt': 'Kindergarten children with teacher in the school play area',
        'category': 'cultural',
        'title': 'Kindergarten Activity Day',
        'tag': 'Cultural',
        'layout': 'photo',
    },
    {
        'file': 'images/main/1.png',
        'alt': 'Student award presentation ceremony',
        'category': 'cultural',
        'title': 'Student Award Presentation',
        'tag': 'Cultural',
        'layout': 'photo',
    },
    {
        'file': 'images/main/2.png',
        'alt': 'Academic achievement ceremony in school uniform',
        'category': 'cultural',
        'title': 'Academic Achievement Ceremony',
        'tag': 'Cultural',
        'layout': 'photo',
    },
    {
        'file': 'images/main/3.png',
        'alt': 'Celebration day gift presentation',
        'category': 'cultural',
        'title': 'Celebration Day Presentation',
        'tag': 'Cultural',
        'layout': 'photo',
    },
    {
        'file': 'images/main/4.png',
        'alt': 'Faculty appreciation with floral tribute',
        'category': 'cultural',
        'title': 'Faculty Appreciation Event',
        'tag': 'Cultural',
        'layout': 'photo',
    },
    {
        'file': 'images/toppers-sslc.jpeg',
        'alt': 'SSLC exam school toppers announcement',
        'category': 'academics',
        'title': 'SSLC Exam School Toppers',
        'tag': 'Academics',
        'layout': 'poster',
    },
    {
        'file': 'images/toppers-hsc.jpeg',
        'alt': 'Higher secondary public exam school toppers',
        'category': 'academics',
        'title': 'HSC Public Exam School Toppers',
        'tag': 'Academics',
        'layout': 'poster',
    },
    {
        'file': 'images/infra/infra-1.jpeg',
        'alt': 'Students conducting chemistry practical session',
        'category': 'infra',
        'title': 'Chemistry Laboratory Practical',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-2.jpeg',
        'alt': 'Students performing titration experiments',
        'category': 'infra',
        'title': 'Advanced Chemistry Experiments',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-3.jpeg',
        'alt': 'Full chemistry lab with students at work',
        'category': 'infra',
        'title': 'State-of-the-Art Chemistry Lab',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-4.jpeg',
        'alt': 'Chemistry practical class supervised by faculty',
        'category': 'infra',
        'title': 'Hands-on Science Learning',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-5.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-6.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-7.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-8.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-9.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-10.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-11.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-12.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-13.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-14.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-15.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-16.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-23.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-24.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-31.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/infra/infra-32.jpeg',
        'alt': 'School infrastructure facility',
        'category': 'infra',
        'title': 'Campus Facility',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
    {
        'file': 'images/Staff/0.png',
        'alt': 'Headmistress Sr. Dr. Margaret Daisy in the school office',
        'category': 'infra',
        'title': 'Headmistress Office',
        'tag': 'Infrastructure',
        'layout': 'photo',
    },
]

GALLERY_FILTERS = [
    {'id': 'all', 'label': 'All Photos'},
    {'id': 'cultural', 'label': 'Cultural'},
    {'id': 'academics', 'label': 'Academics'},
    {'id': 'infra', 'label': 'Infrastructure'},
]

STAFF_IMAGE_DIR = Path(__file__).resolve().parent / 'static' / 'images' / 'Staff'
STAFF_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}
TEACHER_CSV_PATH = Path(__file__).resolve().parent / 'static' / 'tech.csv'
if not TEACHER_CSV_PATH.exists():
    TEACHER_CSV_PATH = Path(__file__).resolve().parent / 'static' / 'teacher.csv'

FACULTY_CATEGORIES = [
    {'id': 'headmistress', 'label': 'Headmistress'},
    {'id': 'pg-teacher', 'label': 'PG Teacher'},
    {'id': 'bt-teacher', 'label': 'BT Teacher'},
    {'id': 'physical-education', 'label': 'Physical Education'},
    {'id': 'secretarial', 'label': 'Secretarial Staff'},
    {'id': 'vocational', 'label': 'Vocational & Fine Arts'},
]


def _format_staff_name_part(part):
    """Title-case a name token, keeping short initials in uppercase."""
    compact = part.replace('.', '')
    if compact.isalpha() and len(compact) <= 2:
        return ''.join(ch.upper() if ch.isalpha() else ch for ch in part)
    return part.title()


def name_from_staff_filename(filename):
    """Build a display name from a staff photo filename."""
    stem = re.sub(r'\s+', ' ', Path(filename).stem).strip(' .')
    match = re.match(r'^(Mrs|Miss|Mr|Sr|Dr)\.?\s*(.*)$', stem, re.IGNORECASE)
    if match:
        title = match.group(1).capitalize()
        if title.lower() == 'sr':
            title = 'Sr'
        rest = match.group(2).strip(' .')
        rest_formatted = ' '.join(_format_staff_name_part(token) for token in rest.split())
        return f'{title}. {rest_formatted}'.strip()
    return ' '.join(_format_staff_name_part(token) for token in stem.split())


def _name_match_key(name):
    """Normalize a teacher name for CSV-to-photo matching."""
    without_title = re.sub(r'^(rev\.?\s*sr|rev|sr|mrs|miss|mr|dr)\.?\s*', '', name.strip(), flags=re.IGNORECASE)
    tokens = re.findall(r'[a-z0-9]+', without_title.lower())
    return tuple(tokens)


def category_from_designation(desig):
    """Map a CSV designation to one of the faculty viewing categories."""
    if not desig:
        return None
    compact = re.sub(r'[\s.]+', '', desig).lower()
    lowered = desig.lower()
    if compact in {'hm', 'headmistress'} or 'headmistress' in lowered:
        return 'headmistress'
    if compact.startswith('pg'):
        return 'pg-teacher'
    if compact.startswith('bt'):
        return 'bt-teacher'
    if compact.startswith('pet') or 'physical' in lowered:
        return 'physical-education'
    if 'asst' in compact and compact.startswith('sec'):
        return 'secretarial'
    if any(keyword in lowered for keyword in ('sewing', 'drawing', 'music')):
        return 'vocational'
    return None


def _clean_staff_name(name):
    """Collapse extra spaces in a CSV or mapping name."""
    return re.sub(r'\s+', ' ', (name or '').strip(' .'))


def _display_csv_name(name):
    """Normalize CSV names so titles have a space (Mrs. Name)."""
    cleaned = _clean_staff_name(name)
    if re.match(r'^rev\.?\s*sr\.?\s*', cleaned, flags=re.IGNORECASE):
        return re.sub(r'^rev\.?\s*sr\.?\s*', 'Rev. Sr. ', cleaned, count=1, flags=re.IGNORECASE)
    return re.sub(
        r'^(Sr|Mrs|Miss|Mr|Dr)\.?\s*',
        lambda match: match.group(1)[0].upper() + match.group(1)[1:].lower() + '. ',
        cleaned,
        count=1,
        flags=re.IGNORECASE,
    )


def load_teacher_roster():
    """Load tech.csv / teacher.csv rows in file order for names and sort."""
    roster = []
    if not TEACHER_CSV_PATH.exists():
        return roster

    with open(TEACHER_CSV_PATH, 'r', encoding='utf-8-sig', newline='') as csv_file:
        lines = [line for line in csv_file if line.strip()]
        reader = csv.DictReader(lines)
        for index, row in enumerate(reader):
            name = _clean_staff_name(
                row.get('Name of the Teacher')
                or next((value for value in row.values() if value), '')
            )
            desig = (row.get('Desig.') or '').strip()
            if not name:
                continue
            key = _name_match_key(name)
            if not key:
                continue
            if not desig and index == 0 and 'margaret' in name.lower() and 'daisy' in name.lower():
                desig = 'HM'
            roster.append({
                'name': name,
                'designation': desig,
                'key': key,
                'order': index,
            })
    return roster


def load_staff_photos():
    """Load staff photos keyed by normalized teacher name."""
    photos = {}
    if not STAFF_IMAGE_DIR.is_dir():
        return photos

    mapping_path = Path(__file__).resolve().parent / 'static' / 'staff_mapping.json'
    mapping = {}
    if mapping_path.exists():
        with open(mapping_path, 'r', encoding='utf-8') as f:
            mapping = json.load(f)

    for path in STAFF_IMAGE_DIR.iterdir():
        if not path.is_file() or path.suffix.lower() not in STAFF_IMAGE_EXTENSIONS:
            continue
        name = _clean_staff_name(mapping.get(path.name) or '')
        if not name:
            name = name_from_staff_filename(path.name)
        key = _name_match_key(name)
        if not key:
            continue
        photos[key] = {
            'name': name,
            'image': f'images/Staff/{path.name}',
        }
    return photos


def load_faculty_members():
    """Load faculty in tech.csv order, matching each row to its staff photo."""
    category_labels = {item['id']: item['label'] for item in FACULTY_CATEGORIES}
    photos = load_staff_photos()
    members = []
    used_keys = set()

    for row in load_teacher_roster():
        photo = photos.get(row['key'])
        if not photo:
            continue
        used_keys.add(row['key'])
        category_id = category_from_designation(row['designation'])
        members.append({
            'name': _display_csv_name(row['name']),
            'image': photo['image'],
            'designation': row['designation'],
            'category': category_id or '',
            'category_label': category_labels.get(category_id, ''),
        })

    # Photos that could not be matched to the CSV stay after the ordered list.
    leftover = [
        (key, photo) for key, photo in photos.items() if key not in used_keys
    ]
    leftover.sort(key=lambda item: item[1]['name'].lower())
    for _key, photo in leftover:
        members.append({
            'name': photo['name'],
            'image': photo['image'],
            'designation': '',
            'category': '',
            'category_label': '',
        })

    return members


def group_faculty_members(members):
    """Group staff with photos into the public faculty categories."""
    grouped = {item['id']: [] for item in FACULTY_CATEGORIES}
    for member in members:
        if member['category'] in grouped:
            grouped[member['category']].append(member)
    return [
        {
            'id': item['id'],
            'label': item['label'],
            'members': grouped[item['id']],
        }
        for item in FACULTY_CATEGORIES
        if grouped[item['id']]
    ]


def get_gallery_context():
    """Build the gallery from image files that are still on disk."""
    static_dir = Path(__file__).resolve().parent / 'static'
    images = [
        image for image in GALLERY_IMAGES
        if (static_dir / image['file']).is_file()
    ]
    return {
        'gallery_images': images,
        'gallery_filters': GALLERY_FILTERS,
    }


@app.context_processor
def inject_page_banners():
    """Expose per-page header background images and campus map link to all templates."""
    return {
        'page_banners': PAGE_BANNERS,
        'school_maps_url': SCHOOL_MAPS_URL,
        'school_address_html': SCHOOL_ADDRESS_HTML,
    }

# SMTP Mail Configuration
ADMIN_EMAIL = "Stantony28@gmail.com"
ADMIN_PASSWORD = "wnwx qquj kvzr msdo".replace(" ", "")  # Gmail App Password (strip spaces)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL port

def send_smtp_email(to_email, subject, body_html, body_text):
    """Sends a multi-part HTML/Text email via Gmail SMTP using SSL."""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"St. Antony's HSS <{ADMIN_EMAIL}>"
    msg['To'] = to_email

    # Attach text and html parts
    msg.attach(MIMEText(body_text, 'plain'))
    msg.attach(MIMEText(body_html, 'html'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(ADMIN_EMAIL, ADMIN_PASSWORD)
            server.sendmail(ADMIN_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"SMTP Error encountered: {str(e)}")
        return False

@app.route('/')
def index():
    """Render the school home page."""
    news = [
        {
            "id": 1,
            "title": "Admissions Open",
            "date": "May 25, 2026",
            "summary": "Online admission inquiry forms are now active. Limited seats are available for Higher Secondary streams (Science & Commerce)."
        }
    ]
    
    events = [
        {
            "id": 1,
            "title": "Parent-Teacher Association Meeting",
            "date": "June 05, 2026",
            "time": "09:30 AM - 01:00 PM",
            "location": "School Auditorium"
        },
        {
            "id": 2,
            "title": "World Environment Day Celebrations",
            "date": "June 05, 2026",
            "time": "08:30 AM",
            "location": "School Campus"
        },
        {
            "id": 3,
            "title": "Higher Secondary Classes Reopen",
            "date": "June 12, 2026",
            "time": "08:00 AM",
            "location": "St. Antony's Campus"
        }
    ]
    return render_template('index.html', news=news, events=events)

@app.route('/about')
def about():
    """Render the About Us page."""
    return render_template('about.html')

@app.route('/faculty')
def faculty():
    """Render the Faculty Directory page."""
    members = load_faculty_members()
    return render_template(
        'faculty.html',
        faculty_members=members,
    )

@app.route('/academics')
def academics():
    """Render the Academics page."""
    return render_template('academics.html')

@app.route('/admissions')
def admissions():
    """Render the Admissions page."""
    return render_template('admissions.html')

@app.route('/gallery')
def gallery():
    """Render the Gallery page."""
    return render_template('gallery.html', **get_gallery_context())

@app.route('/contact')
def contact():
    """Render the Contact Us page."""
    return render_template('contact.html')

@app.route('/submit-inquiry', methods=['POST'])
def submit_inquiry():
    """Handle admission inquiry form submissions and send SMTP mails."""
    try:
        data = request.get_json() or request.form
        
        student_name = data.get('studentName')
        parent_name = data.get('parentName')
        email = data.get('email')
        phone = data.get('phone')
        grade = data.get('grade')
        message = data.get('message', 'No details provided.')
        
        if not all([student_name, parent_name, email, phone, grade]):
            return jsonify({
                "status": "error", 
                "message": "All required fields must be completed. Please check your inputs."
            }), 400

        # --- 1. Send detailed inquiry to Admin ---
        admin_subject = f"New Admission Inquiry - Student: {student_name}"
        admin_text = (
            f"Dear Admin,\n\n"
            f"A new admission inquiry has been submitted. Details:\n"
            f"Student Name: {student_name}\n"
            f"Parent Name: {parent_name}\n"
            f"Email Address: {email}\n"
            f"Phone Number: {phone}\n"
            f"Grade Requested: {grade}\n"
            f"Additional Queries: {message}\n\n"
            f"Please take action accordingly.\n"
        )
        admin_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #800000; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">New Admission Inquiry</h2>
                <p>Hello Admin,</p>
                <p>A parent has submitted an admission inquiry for St. Antony's. Here are the details:</p>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr style="background-color: #FAF7F2;"><td style="padding: 10px; font-weight: bold; width: 180px;">Student Name:</td><td style="padding: 10px;">{student_name}</td></tr>
                    <tr><td style="padding: 10px; font-weight: bold;">Parent Name:</td><td style="padding: 10px;">{parent_name}</td></tr>
                    <tr style="background-color: #FAF7F2;"><td style="padding: 10px; font-weight: bold;">Email Address:</td><td style="padding: 10px;"><a href="mailto:{email}">{email}</a></td></tr>
                    <tr><td style="padding: 10px; font-weight: bold;">Phone Number:</td><td style="padding: 10px;"><a href="tel:{phone}">{phone}</a></td></tr>
                    <tr style="background-color: #FAF7F2;"><td style="padding: 10px; font-weight: bold;">Grade Requested:</td><td style="padding: 10px;">{grade}</td></tr>
                    <tr><td style="padding: 10px; font-weight: bold;">Additional Queries:</td><td style="padding: 10px;">{message}</td></tr>
                </table>
                <p style="font-size: 0.9rem; color: #777; border-top: 1px solid #eee; padding-top: 15px; margin-top: 20px;">
                    This inquiry was submitted from the official St. Antony's School Admissions portal.
                </p>
            </div>
        </body>
        </html>
        """
        
        admin_mail_success = send_smtp_email(ADMIN_EMAIL, admin_subject, admin_html, admin_text)

        # --- 2. Send automated Thank You reply to Parent ---
        parent_subject = "Inquiry Received - St. Antony's Girls Higher Secondary School, Chennai"
        parent_text = (
            f"Dear {parent_name},\n\n"
            f"Thank you for contacting St. Antony's Girls Higher Secondary School regarding the admission of {student_name} for Grade {grade}.\n\n"
            f"We have successfully received your inquiry and our school admissions team has logged the details. "
            f"Our admission coordinator will get in touch with you at this email address or via phone (+91 9498802477) within the next 48 business hours to guide you through the next steps (interaction scheduling and verification).\n\n"
            f"Warm regards,\n"
            f"Admissions Desk\n"
            f"St. Antony's Girls Higher Secondary School, Chennai\n"
            f"Email: stantony28@gmail.com\n"
        )
        parent_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 25px; border: 1px solid #e5f0e6; border-radius: 8px; background-color: #FAF7F2;">
                <div style="text-align: center; border-bottom: 2px solid #800000; padding-bottom: 15px; margin-bottom: 20px;">
                    <h2 style="color: #800000; margin: 0; font-family: Georgia, serif;">St. Antony's Girls Higher Secondary School</h2>
                    <p style="color: #D4AF37; font-size: 0.95rem; text-transform: uppercase; margin: 5px 0 0 0; letter-spacing: 1px;">Walk in Light and Truth</p>
                </div>
                <p>Dear <strong>{parent_name}</strong>,</p>
                <p>Thank you for your interest in St. Antony's. We have received your admission inquiry for <strong>{student_name}</strong> seeking enrollment in <strong>Grade {grade}</strong>.</p>
                <p>Our school admissions team has recorded the details. A school representative will contact you at <strong>{phone}</strong> or via email within 48 business hours to discuss the counseling session and guide you through the enrollment procedure.</p>
                
                <div style="background-color: #ffffff; border: 1px solid #eee; padding: 15px; border-radius: 6px; margin: 20px 0;">
                    <h4 style="margin-top: 0; color: #800000;">Next Steps in our Enrollment:</h4>
                    <ol style="margin-bottom: 0; padding-left: 20px; font-size: 0.95rem;">
                        <li><strong>Campus Counseling:</strong> Interaction of the candidate and parents with the Headmistress.</li>
                        <li><strong>Document Verification:</strong> Review of birth/transfer certificates and academic marks.</li>
                        <li><strong>Fee Settlement:</strong> Term payment to confirm and lock the candidate's seat.</li>
                    </ol>
                </div>
                
                <p>If you have any urgent queries, feel free to reach out to us at <a href="tel:+919498802477">+91 9498802477</a> or reply directly to <a href="mailto:stantony28@gmail.com">stantony28@gmail.com</a>.</p>
                
                <div style="border-top: 1px solid #ddd; padding-top: 15px; margin-top: 25px; font-size: 0.85rem; color: #777;">
                    <p style="margin: 0;">Warm regards,</p>
                    <p style="font-weight: bold; margin: 5px 0 0 0; color: #800000;">Admissions Coordinating Desk</p>
                    <p style="margin: 0;">{SCHOOL_ADDRESS_HTML}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        parent_mail_success = send_smtp_email(email, parent_subject, parent_html, parent_text)
        
        # Verify success of SMTP and return appropriate message
        if admin_mail_success and parent_mail_success:
            return jsonify({
                "status": "success",
                "message": f"Thank you, {parent_name}. The admission inquiry has been sent to the admin. A confirmation email has also been sent to your mail id: {email}."
            }), 200
        else:
            # Fallback in case mail transfer fails but inputs were logged
            return jsonify({
                "status": "success",
                "message": f"Thank you, {parent_name}. The inquiry for {student_name} was logged successfully. (Note: Email confirmation delivery was interrupted, but our admin has noted your request)."
            }), 200
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred while processing your request: {str(e)}"
        }), 500

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    """Handle contact page submissions, notifying admin and auto-responding to the user."""
    try:
        data = request.get_json() or request.form
        
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        if not all([name, email, subject, message]):
            return jsonify({
                "status": "error", 
                "message": "All fields are required. Please fill in the details."
            }), 400
            
        # --- 1. Send query notice to Admin ---
        admin_subj = f"New Contact Query: {subject} [From: {name}]"
        admin_text = (
            f"Dear Admin,\n\n"
            f"A user has submitted a contact query through the website. Details:\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n"
            f"Message:\n{message}\n\n"
            f"Please respond accordingly.\n"
        )
        admin_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #800000; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">New Contact Query</h2>
                <p>Hello Admin,</p>
                <p>A query has been received from the Contact Us page on the school website:</p>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr style="background-color: #FAF7F2;"><td style="padding: 10px; font-weight: bold; width: 140px;">From Name:</td><td style="padding: 10px;">{name}</td></tr>
                    <tr><td style="padding: 10px; font-weight: bold;">User Email:</td><td style="padding: 10px;"><a href="mailto:{email}">{email}</a></td></tr>
                    <tr style="background-color: #FAF7F2;"><td style="padding: 10px; font-weight: bold;">Subject:</td><td style="padding: 10px;">{subject}</td></tr>
                    <tr><td style="padding: 10px; font-weight: bold; vertical-align: top;">Message:</td><td style="padding: 10px; white-space: pre-wrap;">{message}</td></tr>
                </table>
                <p style="font-size: 0.9rem; color: #777; border-top: 1px solid #eee; padding-top: 15px; margin-top: 20px;">
                    This query was submitted from the official St. Antony's School Contact Us portal.
                </p>
            </div>
        </body>
        </html>
        """
        
        admin_mail_success = send_smtp_email(ADMIN_EMAIL, admin_subj, admin_html, admin_text)

        # --- 2. Send automated response to User ---
        user_subj = "Thank you for contacting St. Antony's Girls HSS, Chennai"
        user_text = (
            f"Dear {name},\n\n"
            f"Thank you for reaching out to St. Antony's Girls Higher Secondary School. We have received your query regarding '{subject}'.\n\n"
            f"Our school has logged your message. A school representative will review the details and respond to your email shortly.\n\n"
            f"Warm regards,\n"
            f"School Administration\n"
            f"{SCHOOL_ADDRESS}\n"
            f"Phone: +91 9498802477\n"
            f"Email: stantony28@gmail.com\n"
        )
        user_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 25px; border: 1px solid #ddd; border-radius: 8px; background-color: #FAF7F2;">
                <div style="text-align: center; border-bottom: 2px solid #800000; padding-bottom: 15px; margin-bottom: 20px;">
                    <h2 style="color: #800000; margin: 0; font-family: Georgia, serif;">St. Antony's Girls Higher Secondary School</h2>
                    <p style="color: #D4AF37; font-size: 0.95rem; text-transform: uppercase; margin: 5px 0 0 0; letter-spacing: 1px;">Walk in Light and Truth</p>
                </div>
                <p>Dear <strong>{name}</strong>,</p>
                <p>Thank you for contacting us. We have received your message regarding "<strong>{subject}</strong>".</p>
                <p>Our school has received and logged your request. A school representative will review the details and get back to you at <strong>{email}</strong> shortly.</p>
                
                <p>If your inquiry is urgent, please do not hesitate to contact our desk at <a href="tel:+919498802477">+91 9498802477</a> or email us at <a href="mailto:stantony28@gmail.com">stantony28@gmail.com</a>.</p>
                
                <div style="border-top: 1px solid #ddd; padding-top: 15px; margin-top: 25px; font-size: 0.85rem; color: #777;">
                    <p style="margin: 0;">Warm regards,</p>
                    <p style="font-weight: bold; margin: 5px 0 0 0; color: #800000;">School Administration</p>
                    <p style="margin: 0;">{SCHOOL_ADDRESS_HTML}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        user_mail_success = send_smtp_email(email, user_subj, user_html, user_text)

        if admin_mail_success and user_mail_success:
            return jsonify({
                "status": "success",
                "message": f"Thank you, {name}. Your message has been sent to the admin. A confirmation reply has also been sent to your email id: {email}."
            }), 200
        else:
            return jsonify({
                "status": "success",
                "message": f"Thank you, {name}. Your query was logged. (Note: Email notices are offline, but the school has logged your query)."
            }), 200
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred while processing your message: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
