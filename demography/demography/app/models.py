from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, False),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, True),
            'Administrator': (0xff, True)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Plant(db.Model):
    __tablename__ = 'plant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    matrixnumber = db.Column(db.Integer(64), unique=True, index=True)
    matrix = db.Column(db.Text)
    dimension = db.Column(db.Integer)
    matrixclassnumber = db.Column(db.Integer)
    matrixclassorganised = db.Column(db.String(64))
    matrixsplit = db.Column(db.String(64))
    classnames = db.Column(db.Text)
    observation = db.Column(db.String(250))
    matrixcomposite = db.Column(db.String(64))
    matrixtreatment = db.Column(db.String(84))
    matrixcaptivity = db.Column(db.String(10))
    matrixstartyear = db.Column(db.Integer)
    matrixstartseason = db.Column(db.String(10))
    matrixstartmonth = db.Column(db.Integer)
    matrixendyear = db.Column(db.Integer)
    matrixendseason = db.Column(db.Integer)
    matrixendmonth = db.Column(db.String(16))
    studiedsex = db.Column(db.String(4))
    population = db.Column(db.String(64))
    latdeg = db.Column(db.Integer)
    latmin = db.Column(db.Integer)
    latsec = db.Column(db.Integer)
    londeg = db.Column(db.Integer)
    lonmin = db.Column(db.Integer)
    lonsec = db.Column(db.Integer)
    latitudedec = db.Column(db.Integer)
    longitudedec = db.Column(db.Integer)
    altitude = db.Column(db.Integer)
    country = db.Column(db.String(64))
    continent = db.Column(db.String(64))
    criteriasize = db.Column(db.String(64))
    criteriaontogeny = db.Column(db.String(64))
    authors = db.Column(db.String(64))
    journal = db.Column(db.String(64))
    yearpublication = db.Column(db.Integer)
    doiisbn = db.Column(db.String(64))
    additionalsource = db.Column(db.String(200))
    enteredby = db.Column(db.String(64))
    entereddate = db.Column(db.String(64))
    source = db.Column(db.String(100))
    statusstudy = db.Column(db.String(64))
    statusstudyref = db.Column(db.String(64))
    statuselsewhere = db.Column(db.String(64))
    statuselsewhereref = db.Column(db.String(64))

    species_id = db.Column(db.Integer, db.ForeignKey("species.name"))
    species = db.relationship("Species", backref="plants")


    def __init__(self, name, matrixnumber, matrix, dimension, matrixclassnumber, matrixclassorganised, matrixsplit, classnames, observation, matrixcomposite, matrixtreatment, matrixcaptivity, matrixstartyear, matrixstartseason, matrixstartmonth, matrixendyear, matrixendseason, matrixendmonth, studiedsex, population, latdeg, latmin, latsec, londeg, lonmin, lonsec, latitudedec, longitudedec, altitude, country, continent, criteriasize, criteriaontogeny, authors, journal, yearpublication, doiisbn, additionalsource, enteredby, entereddate, source, statusstudy, statusstudyref, statuselsewhere, statuselsewhereref):
        """"""
        self.name = name
        self.matrixnumber = matrixnumber
        self.matrix = matrix
        self.dimension = dimension
        self.matrixclassnumber = matrixclassnumber
        self.matrixclassorganised = matrixclassorganised
        self.matrixsplit = matrixsplit
        self.classnames = classnames
        self.observation = observation
        self.matrixcomposite = matrixcomposite
        self.matrixtreatment = matrixtreatment
        self.matrixcaptivity = matrixcaptivity
        self.matrixstartyear = matrixstartyear
        self.matrixstartseason = matrixstartseason
        self.matrixstartmonth = matrixstartmonth
        self.matrixendyear = matrixendyear
        self.matrixendseason = matrixendseason
        self.matrixendmonth = matrixendmonth
        self.studiedsex = studiedsex
        self.population = population
        self.latdeg = latdeg
        self.latmin = latmin
        self.latsec = latsec
        self.londeg = londeg
        self.lonmin = lonmin
        self.lonsec = lonsec
        self.latitudedec = latitudedec
        self.longitudedec = longitudedec
        self.altitude = altitude
        self.country = country
        self.continent = continent
        self.criteriasize = criteriasize
        self.criteriaontogeny = criteriaontogeny
        self.authors = authors
        self.journal = journal
        self.yearpublication = yearpublication
        self.doiisbn = doiisbn
        additionalsource = additionalsource
        self.enteredby = enteredby
        self.entereddate = entereddate
        self.source = source
        self.statusstudy = statusstudy
        self.statusstudyref = statusstudyref
        self.statuselsewhere = statuselsewhere
        self.statuselsewhereref = statuselsewhereref


    def __repr__(self):
        return '<Plant %r>' % self.matrixnumber

class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    speciesauthor = db.Column(db.String(64))
    kingdom = db.Column(db.String(64))
    phylum = db.Column(db.String(64))
    angiogymno = db.Column(db.String(64))
    dicotmonoc = db.Column(db.String(64))
    _class = db.Column(db.String(64))
    _order = db.Column(db.String(64))
    family = db.Column(db.String(64))
    genus = db.Column(db.String(64))
    ecoregion = db.Column(db.String(64))
    growthtype = db.Column(db.String(64))
    growthformraunkiaer = db.Column(db.String(64))
    annualperiodicity = db.Column(db.Integer)
    planttype = db.Column(db.String(64))
    commonname = db.Column(db.String(64))
    originalimageurl = db.Column(db.String(64))

   

    def __init__(self, name, speciesauthor, kingdom, phylum, angiogymno, dicotmonoc, _class, _order, family, genus, ecoregion, growthtype, growthformraunkiaer, annualperiodicity, planttype, commonname, originalimageurl):
        """"""
        self.name = name
        self.speciesauthor = speciesauthor
        self.kingdom = kingdom
        self.phylum = phylum
        self.angiogymno = angiogymno
        self.dicotmonoc = dicotmonoc
        self._class = _class
        self._order = _order
        self.family = family
        self.genus = genus
        self.ecoregion = ecoregion
        self.growthtype = growthtype
        self.growthformraunkiaer = growthformraunkiaer
        self.annualperiodicity = annualperiodicity
        self.planttype = planttype
        self.commonname = commonname
        self.originalimageurl = originalimageurl

    def __repr__(self):
        return '<Species %r>' % self.name





