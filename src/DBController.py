from models.CertsModel import *
from models.HostsModel import *
import sqlite3

class DBController(object):

    def __init__(self) -> None:
        self.DBFILE = "./db/abysswatcher.sqlite3"
        self.CONN = sqlite3.connect(self.DBFILE)
        self.CUR  = self.CONN.cursor()
    
    def __del__(self) -> None:
        self.CUR.close
        self.CONN.close

    def isInitializedDB(self) -> bool:
        self.CUR.execute("select name from sqlite_master where type='table'")
        data = self.CUR.fetchall()
        if len(data) <= 1:
            return False
        else:
            return True

    def initInstall(self) -> None:
        fp = "./sql/init.sql"
        with open(fp, "r") as f:
            initsql = f.read()
            self.CUR.executescript(initsql)

    def getAllHosts(self) -> list:
        sql = """
            select hosts.id, cert_state.state, hosts.name, hosts.url,
                ports.port, certs.begin_date, certs.expire_date, certs.issuer
            from hosts
            left join ports ON hosts.id = ports.host_id
            left join certs ON ports.id = certs.port_id
            left join cert_state ON certs.cert_state = cert_state.id
            """

        self.CUR.execute(sql)
        data = self.CUR.fetchall()
        return data
    
    def getAnyHosts(self, position: int, range: int) -> list:
        sql = """
            select hosts.id, cert_state.state, hosts.name, hosts.url,
                ports.port, certs.begin_date, certs.expire_date, certs.issuer
            from hosts
            left join ports ON hosts.id = ports.host_id
            left join certs ON ports.id = certs.port_id
            left join cert_state ON certs.cert_state = cert_state.id
            LIMIT ?, ?
            """
        self.CUR.execute(sql, (position, range))
        data = self.CUR.fetchall()
        return data

    def setHosts(self, host: RegisterHostModel) -> None:
        name = host.name
        url  = host.url
        # [(443, "https://hoge.com"), (443, "https://huga.com"), ...]
        url_port = list(map(lambda x: tuple([x,url]), host.ports))

        host_sql = "INSERT INTO hosts(name, url) VALUES(?,?)"
        port_sql = """
                    INSERT INTO ports(host_id, port) SELECT hosts.id, ? FROM hosts
                    LEFT JOIN ports ON hosts.id = ports.id
                    WHERE hosts.url = ? 
                   """
        
        self.CUR.execute(host_sql, (name, url))
        self.CUR.executemany(port_sql, url_port)

    def setCert(self, cert: RegisterCertModel):
        sql = """
            INSERT INTO certs(port_id, begin_date, expire_date, begin_unixtime, expire_unixtime, issuer, last_update, cert_state)
            SELECT ports.id, ?, ?, ?, ?, ?, ?, ? 
            from hosts
            left join ports on hosts.id = ports.host_id
            left join certs on ports.id = certs.port_id
            WHERE hosts.url = ? AND ports.port = ?
        """
        args = (cert.sslCertBeginDate, cert.sslCertExpireDate, \
                cert.sslCertBeginUnixTime, cert.sslCertExpireUnixTime, cert.sslCertIssuer, \
                cert.updateCheckTime, cert.sslCertState, cert.url, cert.port)

        self.CUR.execute(sql, args)
    
    def getGenCertModelFromCertId(self, cert_id: int):
        sel_sql = """
               SELECT hosts.url, ports.port
               FROM certs
               LEFT JOIN ports ON certs.port_id = ports.id
               LEFT JOIN hosts ON hosts.id = ports.host_id
               WHERE certs.id = ?
              """
        self.CUR.execute(sel_sql, (cert_id,))
        data = self.CUR.fetchall()
        return data
    
    def updateCert(self, cert: RegisterCertModel, cert_id: int):
        sql = """
            UPDATE certs
            SET begin_date = ?,
                expire_date = ?, 
                begin_unixtime = ?, 
                expire_unixtime = ?,
                issuer = ?, 
                last_update = ?, 
                cert_state = ?
            WHERE id = ?
        """
        args = (cert.sslCertBeginDate, cert.sslCertExpireDate, \
                cert.sslCertBeginUnixTime, cert.sslCertExpireUnixTime, cert.sslCertIssuer, \
                cert.updateCheckTime, cert.sslCertState, cert_id)

        self.CUR.execute(sql, args)


    def getCertStateDanger(self):
        sql = """
        SELECT hosts.name, hosts.url, expire_date, last_update FROM certs
        LEFT JOIN hosts ON certs.port_id = hosts.id
        WHERE cert_state = 3
        ORDER BY expire_date ASC;
        """

        self.CUR.execute(sql)
        data = self.CUR.fetchall()
        return data


    def getCertStateExpired(self):
        sql = """
        SELECT hosts.name, hosts.url, expire_date, last_update FROM certs
        LEFT JOIN hosts ON certs.port_id = hosts.id
        WHERE cert_state = 4
        ORDER BY expire_date ASC;
        """

        self.CUR.execute(sql)
        data = self.CUR.fetchall()
        return data


    def commit(self) ->None:
        self.CONN.commit()
