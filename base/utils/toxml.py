#coding=utf-8
import pymysql
import xml.dom.minidom
import sys, os

#sys.setdefaultencoding('utf8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

class toxml(object):

    def get_conn(self):
        host = 'localhost'
        port = 3306
        user = 'root'
        password = '123456'
        database = 'easytest'

        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
        return conn

    def query(self, cur, sql, args):
        cur.execute(sql, args)
        return cur.fetchall()

    def data_list(self, result):

        names = 'processingno testdataname sender receiver serial seqno processid processtype businesstype processstatus processdate processtime futuresid clienttype clientregion foreignclientmode ' \
                'idtype idoriginal idtransformed nationality province city workunit position workproperty clientname clientnameeng ledgermanagename exclientidrefname ledgermanageid ' \
                'assetmgrclienttype assetmgrtype directionalassetclienttype ledgermanagebank ledgermanagebankaccount investvariety investscale assetmgrfund durationstartdate durationenddate ' \
                'assetmgrstarttime assetmgrexpirytime registryaddrcountry registryaddrprovince registryaddrcity registryaddraddress gender birthday nocid nocidextracode hasidverified companyid ' \
                'compclientid exchangeid agencyregid exagencyregid excompanyid exclientidtype exclientid organtype taxno licenseno businessperiod registrycapital registrycurrency hasboard legalperson legalidtype legalid legalbirthday legalnationality legalprovince ' \
                'legalcity legaladdrzipcode legalphonecountrycode legalphoneareacode legalphonenumber ledgercontactname ledgeridtype ledgerid ledgerphonecountrycode ledgerphoneareacode ledgerphonenumber assetmgrname assetmgridtype assetmgrid assetmgrmgrphonecountrycode ' \
                'assetmgrmgrphoneareacode assetmgrmgrphonenumber contactperson classify phonecountrycode phoneareacode phonenumber faxcountrycode faxareacode faxnumber addrcountry addrprovince addrcity ' \
                'addraddress addrzipcode email website authname authidtype authid authphonecountrycode authphoneareacode authphonenumber authnationality authprovince authcity authemail authaddrcountry authaddrprovince authaddrcity authaddraddress authaddrzipcode ' \
                'ordername orderidtype orderid orderphonecountrycode orderphoneareacode orderphonenumber ordernationality orderprovince ordercity orderemail orderaddrcountry orderaddrprovince orderaddrcity orderaddraddress orderaddrzipcode fundname fundidtype fundid fundphonecountrycode fundphoneareacode fundphonenumber fundnationality fundprovince ' \
                'fundcity fundemail fundaddrcountry fundaddrprovince fundaddrcity fundaddraddress fundaddrzipcode billname billidtype billid billphonecountrycode billphoneareacode billphonenumber billnationality billprovince billcity billemail billaddrcountry billaddrprovince billaddrcity ' \
                'billaddraddress billaddrzipcode departmentname departmentcode hastrustee trusteeregistrycapital trusteeregcurrency trusteename trusteenocid trusteetaxno trusteelicenseno trusteebankname trusteebankaccount trusteecountry trusteeprovince trusteecity trusteeaddress trusteezipcode trusteelegalperson ' \
                'trusteelegalidtype trusteelegalid trusteelegalphonecountrycode trusteelegalphoneareacode trusteelegalphonenumber trusteeauthname trusteeauthidtype trusteeauthid trusteeauthphonecountrycode trusteeauthphoneareacode trusteeauthphonenumber trusteecontactname trusteecontactidtype trusteecontactid trusteecontactphonecountrycode ' \
                'trusteecontactphoneareacode trusteecontactphonenumber cfmmcreturncode cfmmcreturnmsg exreturncode exreturnmsg opendate receivefilename capitalscale hasshareholders hasfundmgr fundmgrname fundmgridtype fundmgrid fundmgrcountrycode fundmgrareacode fundmgrphone fundmgraddrcountry fundmgraddrprovince fundmgraddrcity fundmgraddr hasinvestadv ' \
                'investadvname investadvidtype investadvid investadvcountrycode investadvareacode investadvphone investadvaddrcountry investadvaddrprovince investadvaddrcity investadvaddr ' \
                'appropriatype industryid bankid accountno accountname branchname accountcurrency'.split()
        managerList = [dict(zip(names, t)) for t in result]
        print(managerList)
        return managerList

    def read_persondata_to_xml(self, processingno):
        conn = self.get_conn()
        cur = conn.cursor()
        try:
            #sql = 'select* from base_seqprocess'
            sql = 'select* from base_seqprocess b where b.processingno= %s' % processingno
            results = self.query(cur=cur, sql=sql, args=None)
            result = list(results)
            print(result)
            managerList = self.data_list(result)
        except Exception as e:
            raise e
        finally:
            conn.close()
        for i in managerList:
            doc = xml.dom.minidom.Document()
            package_list = doc.createElement('package_list')
            package_list.setAttribute('version', '1.3')
            package_list.setAttribute('from', 'cfmmc')
            package_list.setAttribute('to', i['exchangeid'])
            doc.appendChild(package_list)
            package = doc.createElement('package')
            package.setAttribute('seqserial', '1')
            package.setAttribute('seqno',  str(i['seqno']))
            package_list.appendChild(package)
            process = doc.createElement('process')
            process.setAttribute('processid', i['processid'])
            process.setAttribute('processstatus', str(i['processstatus']))
            process.setAttribute('processdate', i['processdate'])
            process.setAttribute('processtime', i['processtime'])
            process.setAttribute('processtype', i['processtype'])
            process.setAttribute('businesstype', '1')
            process.setAttribute('cfmmcreturncode', str(i['cfmmcreturncode']))
            process.setAttribute('exreturncode', i['exreturncode'])
            process.setAttribute('exreturnmsg', i['exreturnmsg'])
            package.appendChild(process)
            person_info = doc.createElement('person_info')
            person_info.setAttribute('clientregion', i['clientregion'])
            person_info.setAttribute('foreignclientmode', i['foreignclientmode'])
            person_info.setAttribute('clienttype', i['clienttype'])
            person_info.setAttribute('futuresid', i['futuresid'])
            person_info.setAttribute('exchangeid', i['exchangeid'])
            person_info.setAttribute('companyid', i['companyid'])
            person_info.setAttribute('excompanyid', i['excompanyid'])
            person_info.setAttribute('exclientidtype', i['exclientidtype'])
            person_info.setAttribute('exclientid', i['exclientid'])
            person_info.setAttribute('agencyregid', i['agencyregid'])
            person_info.setAttribute('exagencyregid', i['exagencyregid'])
            person_info.setAttribute('clientname', i['clientname'])
            person_info.setAttribute('nationality', i['nationality'])
            person_info.setAttribute('idtype', i['idtype'])
            person_info.setAttribute('id_original', i['idoriginal'])
            person_info.setAttribute('id_transformed', i['idtransformed'])
            person_info.setAttribute('birthday', i['birthday'])
            person_info.setAttribute('gender', i['gender'])
            person_info.setAttribute('classify', i['classify'])
            person_info.setAttribute('compclientid', i['compclientid'])
            person_info.setAttribute('opendate', i['opendate'])
            person_info.setAttribute('phone_countrycode', i['phonecountrycode'])
            person_info.setAttribute('phone_areacode', i['phoneareacode'])
            person_info.setAttribute('phone_number', i['phonenumber'])
            person_info.setAttribute('addr_zipcode', i['addrzipcode'])
            person_info.setAttribute('addr_country', i['addrcountry'])
            person_info.setAttribute('addr_province', i['addrprovince'])
            person_info.setAttribute('addr_city', i['addrcity'])
            person_info.setAttribute('addr_address', i['addraddress'])
            person_info.setAttribute('order_name', i['ordername'])
            person_info.setAttribute('order_idtype', i['orderidtype'])
            person_info.setAttribute('order_id', i['orderid'])
            person_info.setAttribute('order_phone_countrycode', i['orderphonecountrycode'])
            process.appendChild(person_info)
            bankacc_list = doc.createElement('bankacc_list')
            person_info.appendChild(bankacc_list)
            bankacc = doc.createElement('bankacc')
            bankacc.setAttribute('accountno', i['accountno'])
            bankacc.setAttribute('bankid', i['bankid'])
            bankacc.setAttribute('accountname', i['accountname'])
            bankacc.setAttribute('branchname', i['branchname'])
            bankacc_list.appendChild(bankacc)
        date = i['opendate'].replace('-', '')
        print(date)
        filename = 'cfmmc_%s_%s_%08d.xml' % (i['exchangeid'], date, i['processingno'])
        f = open('E:/TestPlatform/EasyTest-master/base/result/%s' % filename, 'w')
        doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding="gbk")
        f.close()
        return filename

    def read_organdata_to_xml(self, processingno):
        conn = self.get_conn()
        cur = conn.cursor()
        try:
            #sql = 'select* from base_seqprocess'
            sql = 'select* from base_seqprocess b where b.processingno= %s' % processingno
            results = self.query(cur=cur, sql=sql, args=None)
            result = list(results)
            print(result)
            managerList = self.data_list(result)
        except Exception as e:
            raise e
        finally:
            conn.close()
        for i in managerList:
            doc = xml.dom.minidom.Document()
            package_list = doc.createElement('package_list')
            package_list.setAttribute('version', '1.3')
            package_list.setAttribute('from', 'cfmmc')
            package_list.setAttribute('to', i['exchangeid'])
            doc.appendChild(package_list)
            package = doc.createElement('package')
            package.setAttribute('seqserial', '1')
            package.setAttribute('seqno',  str(i['seqno']))
            package_list.appendChild(package)
            process = doc.createElement('process')
            process.setAttribute('processid', i['processid'])
            process.setAttribute('processstatus', str(i['processstatus']))
            process.setAttribute('processdate', i['processdate'])
            process.setAttribute('processtime', i['processtime'])
            process.setAttribute('processtype', i['processtype'])
            process.setAttribute('businesstype', '1')
            process.setAttribute('cfmmcreturncode', str(i['cfmmcreturncode']))
            process.setAttribute('exreturncode', i['exreturncode'])
            process.setAttribute('exreturnmsg', i['exreturnmsg'])
            package.appendChild(process)
            organ_info = doc.createElement('organ_info')
            organ_info.setAttribute('clientregion', i['clientregion'])
            organ_info.setAttribute('foreignclientmode', i['foreignclientmode'])
            organ_info.setAttribute('clienttype', i['clienttype'])
            organ_info.setAttribute('futuresid', i['futuresid'])
            organ_info.setAttribute('exchangeid', i['exchangeid'])
            organ_info.setAttribute('companyid', i['companyid'])
            organ_info.setAttribute('excompanyid', i['excompanyid'])
            organ_info.setAttribute('exclientidtype', i['exclientidtype'])
            organ_info.setAttribute('exclientid', i['exclientid'])
            organ_info.setAttribute('agencyregid', i['agencyregid'])
            organ_info.setAttribute('exagencyregid', i['exagencyregid'])
            organ_info.setAttribute('clientname', i['clientname'])
            organ_info.setAttribute('idtype', i['idtype'])
            organ_info.setAttribute('nocid', i['nocid'])
            organ_info.setAttribute('licenseno', i['licenseno'])
            organ_info.setAttribute('compclientid', i['compclientid'])
            organ_info.setAttribute('organtype', i['organtype'])
            organ_info.setAttribute('taxno', i['taxno'])
            organ_info.setAttribute('registry_currency', i['registrycurrency'])
            organ_info.setAttribute('registrycapital', i['registrycapital'])
            organ_info.setAttribute('businessperiod', i['businessperiod'])
            organ_info.setAttribute('registry_addr_country', i['registryaddrcountry'])
            organ_info.setAttribute('registry_addr_province', i['registryaddrprovince'])
            organ_info.setAttribute('registry_addr_city', i['registryaddrcity'])
            organ_info.setAttribute('registry_addr_address', i['registryaddraddress'])
            organ_info.setAttribute('classify', i['classify'])
            organ_info.setAttribute('opendate', i['opendate'])
            organ_info.setAttribute('contactperson', i['contactperson'])
            organ_info.setAttribute('phone_countrycode', i['phonecountrycode'])
            organ_info.setAttribute('phone_areacode', i['phoneareacode'])
            organ_info.setAttribute('phone_number', i['phonenumber'])
            organ_info.setAttribute('addr_zipcode', i['addrzipcode'])
            organ_info.setAttribute('addr_country', i['addrcountry'])
            organ_info.setAttribute('addr_province', i['addrprovince'])
            organ_info.setAttribute('addr_city', i['addrcity'])
            organ_info.setAttribute('addr_address', i['addraddress'])
            organ_info.setAttribute('order_name', i['ordername'])
            organ_info.setAttribute('order_idtype', i['orderidtype'])
            organ_info.setAttribute('order_id', i['orderid'])
            process.appendChild(organ_info)
            bankacc_list = doc.createElement('bankacc_list')
            organ_info.appendChild(bankacc_list)
            bankacc = doc.createElement('bankacc')
            bankacc.setAttribute('accountno', i['accountno'])
            bankacc.setAttribute('bankid', i['bankid'])
            bankacc.setAttribute('accountname', i['accountname'])
            bankacc.setAttribute('branchname', i['branchname'])
            bankacc_list.appendChild(bankacc)
            businessrange_list = doc.createElement("businessrange_list")
            businessrange_list.setAttribute('industryid', i['industryid'])
            organ_info.appendChild(businessrange_list)
        date = i['opendate'].replace('-', '')
        print(date)
        filename = 'cfmmc_%s_%s_%08d.xml' % (i['exchangeid'], date, i['processingno'])
        f = open('E:/TestPlatform/EasyTest-master/base/result/%s' % filename, 'w')
        doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding="gbk")
        f.close()
        return filename

    def read_specialoragandata_to_xml(self, processingno):
        conn = self.get_conn()
        cur = conn.cursor()
        try:
            sql = 'select* from base_seqprocess b where b.processingno= %s' % processingno
            results = self.query(cur=cur, sql=sql, args=None)
            result = list(results)
            print(result)
            managerList = self.data_list(result)
        except Exception as e:
            raise e
        finally:
            conn.close()
        for i in managerList:
            doc = xml.dom.minidom.Document()
            package_list = doc.createElement('package_list')
            package_list.setAttribute('version', '1.3')
            package_list.setAttribute('from', 'cfmmc')
            package_list.setAttribute('to', i['exchangeid'])
            doc.appendChild(package_list)
            package = doc.createElement('package')
            package.setAttribute('seqserial', '1')
            package.setAttribute('seqno',  str(i['seqno']))
            package_list.appendChild(package)
            process = doc.createElement('process')
            process.setAttribute('processid', i['processid'])
            process.setAttribute('processstatus', str(i['processstatus']))
            process.setAttribute('processdate', i['processdate'])
            process.setAttribute('processtime', i['processtime'])
            process.setAttribute('processtype', i['processtype'])
            process.setAttribute('businesstype', '1')
            process.setAttribute('cfmmcreturncode', str(i['cfmmcreturncode']))
            process.setAttribute('exreturncode', i['exreturncode'])
            process.setAttribute('exreturnmsg', i['exreturnmsg'])
            package.appendChild(process)
            specialorgan_info = doc.createElement('specialorgan_info')
            specialorgan_info.setAttribute('clienttype', i['clienttype'])
            specialorgan_info.setAttribute('futuresid', i['futuresid'])
            specialorgan_info.setAttribute('exchangeid', i['exchangeid'])
            specialorgan_info.setAttribute('companyid', i['companyid'])
            specialorgan_info.setAttribute('excompanyid', i['excompanyid'])
            specialorgan_info.setAttribute('exclientidtype', i['exclientidtype'])
            specialorgan_info.setAttribute('exclientid', i['exclientid'])
            specialorgan_info.setAttribute('clientname', i['clientname'])
            specialorgan_info.setAttribute('clientname_eng', i['clientnameeng'])
            specialorgan_info.setAttribute('legalperson', i['legalperson'])
            specialorgan_info.setAttribute('legal_idtype', i['legalidtype'])
            specialorgan_info.setAttribute('legal_id', i['legalid'])

            specialorgan_info.setAttribute('legal_phone_countrycode', i['legalphonecountrycode'])
            specialorgan_info.setAttribute('legal_phone_areacode', i['legalphoneareacode'])
            specialorgan_info.setAttribute('legal_phone_number', i['legalphonenumber'])
            specialorgan_info.setAttribute('licenseno', i['licenseno'])
            specialorgan_info.setAttribute('nocid', i['nocid'])
            specialorgan_info.setAttribute('nocid_extracode', i['nocidextracode'])
            specialorgan_info.setAttribute('organtype', i['organtype'])
            specialorgan_info.setAttribute('taxno', i['taxno'])
            specialorgan_info.setAttribute('registry_currency', i['registrycurrency'])
            specialorgan_info.setAttribute('registrycapital', i['registrycapital'])
            specialorgan_info.setAttribute('businessperiod', i['businessperiod'])
            specialorgan_info.setAttribute('registry_addr_country', i['registryaddrcountry'])
            specialorgan_info.setAttribute('registry_addr_province', i['registryaddrprovince'])
            specialorgan_info.setAttribute('registry_addr_city', i['registryaddrcity'])
            specialorgan_info.setAttribute('registry_addr_address', i['registryaddraddress'])
            specialorgan_info.setAttribute('classify', i['classify'])
            specialorgan_info.setAttribute('opendate', i['opendate'])
            specialorgan_info.setAttribute('phone_countrycode', i['phonecountrycode'])
            specialorgan_info.setAttribute('phone_areacode', i['phoneareacode'])
            specialorgan_info.setAttribute('phone_number', i['phonenumber'])
            specialorgan_info.setAttribute('addr_zipcode', i['addrzipcode'])
            specialorgan_info.setAttribute('addr_country', i['addrcountry'])
            specialorgan_info.setAttribute('addr_province', i['addrprovince'])
            specialorgan_info.setAttribute('addr_city', i['addrcity'])
            specialorgan_info.setAttribute('addr_address', i['addraddress'])
            specialorgan_info.setAttribute('order_name', i['ordername'])
            specialorgan_info.setAttribute('order_idtype', i['orderidtype'])
            specialorgan_info.setAttribute('order_id', i['orderid'])
            process.appendChild(specialorgan_info)
            bankacc_list = doc.createElement('bankacc_list')
            specialorgan_info.appendChild(bankacc_list)
            bankacc = doc.createElement('bankacc')
            bankacc.setAttribute('accountno', i['accountno'])
            bankacc.setAttribute('bankid', i['bankid'])
            bankacc.setAttribute('accountname', i['accountname'])
            bankacc.setAttribute('branchname', i['branchname'])
            bankacc_list.appendChild(bankacc)
            businessrange_list = doc.createElement("businessrange_list")
            businessrange_list.setAttribute('industryid', i['industryid'])
            specialorgan_info.appendChild(businessrange_list)
            share_holder_list = doc.createElement("share_holder_list")
            specialorgan_info.appendChild(share_holder_list)
            share_holder = doc.createElement('share_holder')
            share_holder.setAttribute("share_holder_type", '1')
            share_holder.setAttribute("share_holder_name", 'share_holder_name_xu_1')
            share_holder.setAttribute("share_holder_idtype", "share_holder_idtype")
            share_holder.setAttribute("share_holder_id", "share_holder_id")
            share_holder.setAttribute("share_holding_ratio", "share_holding_ratio")
            share_holder.setAttribute("share_holding_amount", "share_holding_amount")
            share_holder.setAttribute("product_mgr_name", "product_mgr_name")
            share_holder.setAttribute("product_code", "product_code")
            share_holder.setAttribute("product_scale", "product_scale")
            share_holder_list.appendChild(share_holder)

        date = i['opendate'].replace('-', '')
        print(date)
        filename = 'cfmmc_%s_%s_%08d.xml' % (i['exchangeid'], date, i['processingno'])
        f = open('E:/TestPlatform/EasyTest-master/base/result/%s' % filename, 'w')
        doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding="gbk")
        f.close()
        return filename
if __name__ == "__main__":
    c = toxml()
    processingno = '11'
    #c.read_persondata_to_xml(processingno)
    #c.read_organdata_to_xml(processingno)
    c.read_specialoragandata_to_xml(processingno)

