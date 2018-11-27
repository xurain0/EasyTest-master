#coding=utf-8
from django.shortcuts import render
from base.models import Project, Sign, Environment, Interface, Case, Plan, Report, Seqprocess
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.core import serializers
from lib.execute import Execute
import time, datetime
import json
from django.http import HttpResponse, Http404, StreamingHttpResponse
from base.utils.toxml import toxml
from django.views.generic.list import ListView

# Create your views here.



# 项目增删改查
def project_index(request):
    prj_list = Project.objects.all()
    return render(request, "base/project/index.html", {"prj_list": prj_list})


def project_add(request):
    if request.method == 'POST':
        prj_name = request.POST['prj_name']
        name_same = Project.objects.filter(prj_name=prj_name)
        if name_same:
            messages.error(request, "项目已存在")
        else:
            description = request.POST['description']
            #sign_id = request.POST['sign']
            #sign = Sign.objects.get(sign_id=sign_id)
            #prj = Project(prj_name=prj_name, description=description, sign=sign)
            prj = Project(prj_name=prj_name, description=description)
            prj.save()
            return HttpResponseRedirect("/base/project/")
    sign_list = Sign.objects.all()
    return render(request, "base/project/add.html", {"sign_list": sign_list})

def project_update(request):
    if request.method == 'POST':
        prj_id = request.POST['prj_id']
        prj_name = request.POST['prj_name']
        name_exit = Project.objects.filter(prj_name=prj_name).exclude(prj_id=prj_id)
        if name_exit:
            # messages.error(request, "项目已存在")
            return HttpResponse("项目已存在")
        else:
            description = request.POST['description']
            #sign_id = request.POST['sign_id']
            #sign = Sign.objects.get(sign_id=sign_id)
            #Project.objects.filter(prj_id=prj_id).update(prj_name=prj_name, description=description,sign=sign)
            Project.objects.filter(prj_id=prj_id).update(prj_name=prj_name, description=description)
            return HttpResponseRedirect("/base/project/")
    prj_id = request.GET['prj_id']
    prj = Project.objects.get(prj_id=prj_id)
    #sign_list = Sign.objects.all()
    #return render(request, "base/project/update.html", {"prj": prj, "sign_list": sign_list})
    return render(request, "base/project/update.html", {"prj": prj})

def project_delete(request):
    if request.method == 'GET':
        prj_id = request.GET['prj_id']
        Project.objects.filter(prj_id=prj_id).delete()
        return HttpResponseRedirect("base/project/")

# 加密方式增删改查
def sign_index(request):
    sign_list = Sign.objects.all()
    return render(request, "system/sign_index.html", {"sign_list": sign_list})

def sign_add(request):
    if request.method == 'POST':
        sign_name = request.POST['sign_name']
        description = request.POST['description']
        sign = Sign(sign_name=sign_name, description=description)
        sign.save()
        return HttpResponseRedirect("/base/sign/")
    return render(request, "system/sign_add.html")

# 更新加密方式
def sign_update(request):
    if request.method == 'POST':
        sign_id = request.POST['sign_id']
        sign_name = request.POST['sign_name']
        description = request.POST['description']
        Sign.objects.filter(sign_id=sign_id).update(sign_name=sign_name, description=description)
        return HttpResponseRedirect("/base/sign/")
    sign_id = request.GET['sign_id']
    sign = Sign.objects.get(sign_id=sign_id)
    return render(request, "system/sign_update.html", {"sign": sign})

# 测试环境增删改查
def env_index(request):
    env_list = Environment.objects.all()
    return render(request, "base/env/index.html", {"env_list": env_list})

def env_add(request):
    if request.method == 'POST':
        env_name = request.POST['env_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        #private_key = request.POST['private_key']
        description = request.POST['description']
        #env = Environment(env_name=env_name, url=url, project=project,
        #                   private_key=private_key, description=description)
        env = Environment(env_name=env_name, url=url, project=project,
                          description=description)
        env.save()
        return HttpResponseRedirect("/base/env/")
    prj_list = Project.objects.all()
    return render(request, "base/env/add.html", {"prj_list": prj_list})

# 测试环境更新
def env_update(request):
    if request.method == 'POST':
        env_id = request.POST['env_id']
        env_name = request.POST['env_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        #private_key = request.POST['private_key']
        description = request.POST['description']
        Environment.objects.filter(env_id=env_id).update(env_name=env_name, url=url, project=project, description=description)
        return HttpResponseRedirect("/base/env/")
    env_id = request.GET['env_id']
    env =Environment.objects.get(env_id=env_id)
    prj_list = Project.objects.all()
    return render(request, "base/env/update.html", {"env": env, "prj_list": prj_list})

def env_delete(request):
    if request.method == 'GET':
        env_id = request.GET['env_id']
        Environment.objects.filter(env_id=env_id).delete()
        return HttpResponseRedirect("base/env/")

# 接口增删改查
def interface_index(request):
    if_list = Interface.objects.all()
    return render(request, "base/interface/index.html", {"if_list": if_list})

def interface_add(request):
    if request.method == 'POST':
        if_name = request.POST['if_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        method = request.POST['method']
        data_type = request.POST['data_type']
        #is_sign = request.POST['is_sign']
        description = request.POST['description']
        request_header_data = request.POST['request_header_data']
        request_body_data = request.POST['request_body_data']
        response_header_data = request.POST['response_header_data']
        response_body_data = request.POST['response_body_data']
        interface = Interface(if_name=if_name, url=url, project=project, method=method, data_type=data_type,
                          description=description, request_header_param=request_header_data,
                          request_body_param=request_body_data, response_header_param=response_header_data,
                          response_body_param=response_body_data)
        interface.save()
        return HttpResponseRedirect("/base/interface/")
    prj_list = Project.objects.all()
    return render(request, "base/interface/add.html", {"prj_list": prj_list})

# 接口增删改查
def case_index(request):
    case_list = Case.objects.all()
    return render(request, "base/case/index.html", {"case_list": case_list})

def case_add(request):
    if request.method == 'POST':
        case_name = request.POST['case_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        description = request.POST['description']
        content = request.POST['content']
        case = Case(case_name=case_name, project=project, description=description, content=content)
        case.save()
        return HttpResponseRedirect("/base/case/")
    prj_list = Project.objects.all()
    return render(request, "base/case/add.html", {"prj_list": prj_list})

def case_run(request):
    if request.method == 'POST':
        case_id = request.POST['case_id']
        env_id = request.POST['env_id']
        execute = Execute(case_id, env_id)
        case_result = execute.run_case()
        return JsonResponse(case_result)

# 计划增删改查
def plan_index(request):
    plan_list = Plan.objects.all()
    return render(request, "base/plan/index.html", {"plan_list": plan_list})

def plan_add(request):
    if request.method == 'POST':
        plan_name = request.POST['plan_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        env_id = request.POST['env_id']
        environment = Environment.objects.get(env_id=env_id)
        description = request.POST['description']
        content = request.POST.getlist("case_id")
        plan = Plan(plan_name=plan_name, project=project, environment=environment, description=description, content=content)
        plan.save()
        return HttpResponseRedirect("/base/plan/")
    prj_list = Project.objects.all()
    return render(request, "base/plan/add.html", {"prj_list": prj_list})

def plan_run(request):
    if request.method == 'POST':
        plan_id = request.POST['plan_id']
        plan = Plan.objects.get(plan_id=plan_id)
        env_id = plan.environment.env_id
        case_id_list = eval(plan.content)
        case_num = len(case_id_list)
        content = []
        pass_num = 0
        fail_num = 0
        error_num = 0
        for case_id in case_id_list:
            execute = Execute(case_id, env_id)
            case_result = execute.run_case()
            content.append(case_result)
            if case_result["result"] == "pass":
                pass_num += 1
            if case_result["result"] == "fail":
                fail_num += 1
            if case_result["result"] == "error":
                error_num += 1
        report_name = plan.plan_name + "-" + time.strftime("%Y%m%d%H%M%S")
        if Report.objects.filter(plan=plan):
            Report.objects.filter(plan=plan).update(report_name=report_name, content=content, case_num=case_num,
                                                    pass_num=pass_num, fail_num=fail_num, error_num=error_num)
        else:
            report = Report(plan=plan, report_name=report_name, content=content, case_num=case_num,
                            pass_num=pass_num, fail_num=fail_num, error_num=error_num)
            report.save()
        return HttpResponse(plan.plan_name + " 执行成功！")

def report_index(request):
    plan_id = request.GET['plan_id']
    report = Report.objects.get(plan_id=plan_id)
    report_content = eval(report.content)
    return render(request, "report.html", {"report": report, "report_content": report_content})

def findata(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        get_type = request.GET["type"]
        if get_type == "get_all_if_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 返回字典列表
            if_list = Interface.objects.filter(project=prj_id).all().values()
            # list(if_list)将QuerySet转换成list
            return JsonResponse(list(if_list), safe=False)
        if get_type == "get_if_by_if_id":
            if_id = request.GET["if_id"]
            # 查询并将结果转换为json
            interface = Interface.objects.filter(if_id=if_id).values()
            return JsonResponse(list(interface), safe=False)
        if get_type == "get_env_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 查询并将结果转换为json
            env = Environment.objects.filter(project_id=prj_id).values()
            return JsonResponse(list(env), safe=False)
        if get_type == "get_all_case_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 查询并将结果转换为json
            env = Case.objects.filter(project_id=prj_id).values()
            return JsonResponse(list(env), safe=False)

class ClientTypeData(ListView):

    currentdate = datetime.datetime.today().strftime('%Y-%m-%d')
    currenttime = datetime.datetime.today().strftime('%H:%M:%S')

    def getInfoFromId(self, id18):
        '''从身份证号码中得出个人信息：地址、生日、性别'''

        birthDays = datetime.datetime.strftime(datetime.datetime.strptime(id18[6:14], "%Y%m%d"), "%Y-%m-%d")
        sex = '男' if int(id18[-2]) % 2 else '女'  # 0为女性，1为男性

        return birthDays, sex

    def person_index(request):
        person_list = Seqprocess.objects.filter(clienttype='1')
        return render(request, "data/person/index.html", {"person_list": person_list})

    def person_add(request):

        if request.method == 'POST':
            testdataname = request.POST['testdataname']
            sender = 'cfmmc'
            exchangeid = request.POST['exchangeid']
            if exchangeid == 'S':
                receiver = 'S'
            elif exchangeid == 'N':
                receiver = 'N'
            serial = '1'
            seqno = request.POST['seqno']
            processid = request.POST['processid']
            processstatus = '7'                         #交易所处理中
            processdate = ClientTypeData().currentdate
            processtime = ClientTypeData().currenttime
            processtype = request.POST['processtype']
            businesstype = '1'                          #请求
            futuresid = request.POST['futuresid']
            clienttype = '1'                            #客户类型1，个人客户
            clientregion = request.POST['clientregion']
            foreignclientmode = request.POST['foreignclientmode']
            companyid = request.POST['companyid']
            excompanyid = companyid
            exclientidtype = request.POST['exclientidtype']
            exclientid = ''
            if foreignclientmode == '4':
                agencyregid = '0123'
                exagencyregid = '0123'
            else:
                agencyregid = ''
                exagencyregid = ''
            clientname = request.POST['clientname']
            #nationality = request.POST['nationality']
            if clientregion == '1':
                nationality = 'CHN'
                province = ''
                city = ''
                workunit = ''
                position = ''
                workproperty = ''
                addrcountry = 'CHN'
                addrprovince = 'ShangHai'
                addrcity = 'shanghai'
            elif clientregion == '2':
                nationality = 'HKG'
                province = '香港'
                city = '九龙湾'
                workunit = '期货工作'
                position = '经理'
                workproperty = '私有企业'
                addrcountry = 'HKG'
                addrprovince = 'hk'
                addrcity = 'hk'
            else:
                nationality = 'USA'
                province = 'GodenState'
                city = 'LA'
                workunit = 'NBA player'
                position = 'MVP'
                workproperty = 'GS'
                addrcountry = 'USA'
                addrprovince = 'GodenState'
                addrcity= 'GS'

            idtype = '1'          #身份证
            idoriginal = request.POST['idoriginal']
            idtransformed = idoriginal
            birthday = ClientTypeData().getInfoFromId(idoriginal)[0]
            gender = ClientTypeData().getInfoFromId(idoriginal)[1]
            classify = '1'      #投资者类型
            opendate = processdate
            accountname = clientname
            bankid = '01'
            accountno = request.POST['accountno']
            branchname = request.POST['branchname']

            personInfo = Seqprocess(sender=sender, testdataname=testdataname, exchangeid=exchangeid, receiver=receiver,
                                    serial=serial, seqno=seqno, processid=processid, processstatus=processstatus, processdate=processdate, processtime=processtime,
                                    processtype=processtype, businesstype=businesstype, futuresid=futuresid, clienttype=clienttype, clientregion=clientregion,
                                    foreignclientmode=foreignclientmode, companyid=companyid, excompanyid=excompanyid, exclientidtype=exclientidtype, exclientid=exclientid,
                                    agencyregid=agencyregid, exagencyregid=exagencyregid, clientname=clientname, nationality=nationality, province=province, city=city,
                                    workunit=workunit, position=position, workproperty=workproperty, idtype=idtype, idoriginal=idoriginal, idtransformed=idtransformed,
                                    birthday=birthday, gender=gender, classify=classify, opendate=opendate, addrcountry=addrcountry, addrprovince=addrprovince, addrcity=addrcity,
                                    accountname=accountname, bankid=bankid, accountno=accountno, branchname=branchname)
            personInfo.save()
            return HttpResponseRedirect("base/data/person/")
        person_list = Seqprocess.objects.filter(clienttype='1')
        return render(request, "data/person/add.html", {"person_list": person_list})

    def person_detail(request):
        processingno = request.GET['processingno']
        person_detail = Seqprocess.objects.get(processingno=processingno)
        return render(request, "data/person/detail.html", {"person_detail": person_detail})

    def person_delete(request):
        if request.method == 'GET':
            processingno = request.GET['processingno']
            Seqprocess.objects.filter(processingno=processingno).delete()
            return HttpResponseRedirect("base/data/person/")

    def organ_index(request):
        organ_list = Seqprocess.objects.filter(clienttype='2')
        return render(request, "data/organ/index.html", {"organ_list": organ_list})

    def organ_add(request):
        if request.method == 'POST':
            testdataname = request.POST['testdataname']
            sender = 'cfmmc'
            exchangeid = request.POST['exchangeid']
            if exchangeid == 'S':
                receiver = 'S'
            elif exchangeid == 'N':
                receiver = 'N'
            serial = '1'
            seqno = request.POST['seqno']
            processid = request.POST['processid']
            processstatus = '7'                         #交易所处理中
            processdate = ClientTypeData().currentdate
            processtime = ClientTypeData().currenttime
            processtype = request.POST['processtype']
            businesstype = '1'                          #请求
            futuresid = request.POST['futuresid']
            clienttype = '2'                            #客户类型2，单位客户
            clientregion = request.POST['clientregion']
            foreignclientmode = request.POST['foreignclientmode']
            companyid = request.POST['companyid']
            excompanyid = companyid
            exclientidtype = request.POST['exclientidtype']
            exclientid = ''
            if foreignclientmode == '4':
                agencyregid = '0123'
                exagencyregid = '0123'
            else:
                agencyregid = ''
                exagencyregid = ''
            clientname = request.POST['clientname']
            #nationality = request.POST['nationality']
            if clientregion == '1':
                registryaddrcountry = ''
                registryaddrprovince = ''
                registryaddrcity = ''
                registryaddraddress = ''
            elif clientregion == '2':
                registryaddrcountry = 'HKG'
                registryaddrprovince = '香港'
                registryaddrcity = '九龙湾'
                registryaddraddress = 'hk 1997 No.'
            else:
                registryaddrcountry = 'USA'
                registryaddrprovince = 'GodenState'
                registryaddrcity = 'LA'
                registryaddraddress = 'GS 118 No.'

            idtype = '50'          #组织机构代码证
            licenseno = request.POST['licenseno']
            organtype = '130'
            registrycurrency = 'CNY'
            registrycapital = '100000000.00'
            businessperiod = '2099-12-31'
            classify = '01'      #投资者类型
            opendate = processdate
            industryid = '100'
            accountname = clientname
            bankid = '01'
            accountno = request.POST['accountno']
            branchname = request.POST['branchname']
            organInfo = Seqprocess(sender=sender, testdataname=testdataname, exchangeid=exchangeid, receiver=receiver,
                                    serial=serial, seqno=seqno, processid=processid, processstatus=processstatus, processdate=processdate, processtime=processtime,
                                    processtype=processtype, businesstype=businesstype, futuresid=futuresid, clienttype=clienttype, clientregion=clientregion,
                                    foreignclientmode=foreignclientmode, companyid=companyid, excompanyid=excompanyid, exclientidtype=exclientidtype, exclientid=exclientid,
                                    agencyregid=agencyregid, exagencyregid=exagencyregid, clientname=clientname, registryaddrcountry=registryaddrcountry, registryaddrprovince=registryaddrprovince, registryaddrcity=registryaddrcity,
                                    registryaddraddress=registryaddraddress, licenseno=licenseno, organtype=organtype, idtype=idtype, registrycurrency=registrycurrency, registrycapital=registrycapital,
                                    businessperiod=businessperiod, classify=classify, opendate=opendate, industryid=industryid, accountname=accountname, bankid=bankid, accountno=accountno, branchname=branchname)
            organInfo.save()
            return HttpResponseRedirect("base/data/organ/")
        organ_list = Seqprocess.objects.filter(clienttype='2')
        return render(request, "data/organ/add.html", {"organ_list": organ_list})

    def organ_detail(request):
        processingno = request.GET['processingno']
        organ_detail = Seqprocess.objects.get(processingno=processingno)
        return render(request, "data/organ/detail.html", {"organ_detail": organ_detail})

    def organ_delete(request):
        if request.method == 'GET':
            processingno = request.GET['processingno']
            Seqprocess.objects.filter(processingno=processingno).delete()
            return HttpResponseRedirect("base/data/organ/")

    def specialorgan_index(request):
        specialorgan_list = Seqprocess.objects.filter(clienttype='4')
        return render(request, "data/specialorgan/index.html", {"specialorgan_list": specialorgan_list})

    def specialorgan_add(request):
        if request.method == 'POST':
            testdataname = request.POST['testdataname']
            sender = 'cfmmc'
            exchangeid = request.POST['exchangeid']
            if exchangeid == 'S':
                receiver = 'S'
            elif exchangeid == 'N':
                receiver = 'N'
            serial = '1'
            seqno = request.POST['seqno']
            processid = request.POST['processid']
            processstatus = '7'                         #交易所处理中
            processdate = ClientTypeData().currentdate
            processtime = ClientTypeData().currenttime
            processtype = request.POST['processtype']
            businesstype = '1'                          #请求
            futuresid = request.POST['futuresid']
            clienttype = '4'                            #客户类型2，特殊单位客户
            companyid = request.POST['companyid']
            excompanyid = companyid
            exclientidtype = request.POST['exclientidtype']
            exclientid = ''
            clientname = request.POST['clientname']
            clientnameeng = 'clientnameeng'
            legalperson = request.POST['legalperson']
            legalidtype = '1'
            legalid = request.POST['legalid']
            licenseno =request.POST['licenseno']
            nocid = request.POST['nocid']
            organtype = '01'
            registryaddrcountry = '中国'
            registryaddrprovince = '上海'
            registryaddrcity = '上海'
            registryaddraddress = '上海浦东浦电路500号'
            registrycurrency = 'CNY'
            registrycapital = '100000000.00'
            classify = '01'      #投资者类型
            opendate = processdate
            industryid = '100'
            accountname = clientname
            bankid = '01'
            accountno = request.POST['accountno']
            branchname = request.POST['branchname']

            specialorganInfo = Seqprocess(sender=sender, testdataname=testdataname, exchangeid=exchangeid, receiver=receiver,
                                    serial=serial, seqno=seqno, processid=processid, processstatus=processstatus, processdate=processdate, processtime=processtime,
                                    processtype=processtype, businesstype=businesstype, futuresid=futuresid, clienttype=clienttype, clientnameeng=clientnameeng,
                                    legalperson=legalperson, companyid=companyid, excompanyid=excompanyid, exclientidtype=exclientidtype, exclientid=exclientid,
                                    legalidtype=legalidtype, nocid=nocid, clientname=clientname, registryaddrcountry=registryaddrcountry, registryaddrprovince=registryaddrprovince, registryaddrcity=registryaddrcity,
                                    registryaddraddress=registryaddraddress, licenseno=licenseno, organtype=organtype, registrycurrency=registrycurrency, registrycapital=registrycapital,
                                    legalid=legalid, classify=classify, opendate=opendate, industryid=industryid, accountname=accountname, bankid=bankid, accountno=accountno, branchname=branchname)
            specialorganInfo.save()
            return HttpResponseRedirect("base/data/specialorgan/")
        specialorgan_list = Seqprocess.objects.filter(clienttype='4')
        return render(request, "data/specialorgan/add.html", {"specialorgan_list": specialorgan_list})

    def specialorgan_detail(request):
        processingno = request.GET['processingno']
        specialorgan_detail = Seqprocess.objects.get(processingno=processingno)
        return render(request, "data/specialorgan/detail.html", {"specialorgan_detail": specialorgan_detail})

    def specialorgan_delete(request):
        if request.method == 'GET':
            processingno = request.GET['processingno']
            Seqprocess.objects.filter(processingno=processingno).delete()
            return HttpResponseRedirect("base/data/specialorgan/")

    def asset_index(request):
        asset_list = Seqprocess.objects.filter(clienttype='5')
        return render(request, "data/asset/index.html", {"asset_list": asset_list})

    def asset_add(request):
        if request.method == 'POST':
            testdataname = request.POST['testdataname']
            sender = 'cfmmc'
            exchangeid = request.POST['exchangeid']
            if exchangeid == 'S':
                receiver = 'S'
            elif exchangeid == 'N':
                receiver = 'N'
            serial = '1'
            seqno = request.POST['seqno']
            processid = request.POST['processid']
            processstatus = '7'                         #交易所处理中
            processdate = ClientTypeData().currentdate
            processtime = ClientTypeData().currenttime
            processtype = request.POST['processtype']
            businesstype = '1'                          #请求
            futuresid = request.POST['futuresid']
            clienttype = '5'                            #客户类型5，资管客户
            clientregion = request.POST['clientregion']
            companyid = request.POST['companyid']
            excompanyid = companyid
            exclientidtype = request.POST['exclientidtype']
            exclientid = ''
            clientname = request.POST['clientname']
            nationality = 'CHN'
            idtype = ''
            idoriginal = request.POST['idoriginal']
            idtransformed = idoriginal
            birthday = ClientTypeData().getInfoFromId(idoriginal)[0]
            gender = ClientTypeData().getInfoFromId(idoriginal)[1]
            nocid = ''

            if clientregion == '1':
                registryaddrcountry = ''
                registryaddrprovince = ''
                registryaddrcity = ''
                registryaddraddress = ''
            elif clientregion == '2':
                registryaddrcountry = 'HKG'
                registryaddrprovince = '香港'
                registryaddrcity = '九龙湾'
                registryaddraddress = 'hk 1997 No.'
            else:
                registryaddrcountry = 'USA'
                registryaddrprovince = 'GodenState'
                registryaddrcity = 'LA'
                registryaddraddress = 'GS 118 No.'

            idtype = '50'          #组织机构代码证
            licenseno = request.POST['licenseno']
            organtype = '130'
            registrycurrency = 'CNY'
            registrycapital = '100000000.00'
            businessperiod = '2099-12-31'
            classify = '01'      #投资者类型
            opendate = processdate
            industryid = '100'
            accountname = clientname
            bankid = '01'
            accountno = request.POST['accountno']
            branchname = request.POST['branchname']

            assetInfo = Seqprocess(sender=sender, testdataname=testdataname, exchangeid=exchangeid, receiver=receiver,
                                    serial=serial, seqno=seqno, processid=processid, processstatus=processstatus, processdate=processdate, processtime=processtime,
                                    processtype=processtype, businesstype=businesstype, futuresid=futuresid, clienttype=clienttype, clientregion=clientregion,
                                    idoriginal=idoriginal, companyid=companyid, excompanyid=excompanyid, exclientidtype=exclientidtype, exclientid=exclientid,
                                    nationality=nationality, idtype=idtype, clientname=clientname, registryaddrcountry=registryaddrcountry, registryaddrprovince=registryaddrprovince, registryaddrcity=registryaddrcity,
                                    registryaddraddress=registryaddraddress, licenseno=licenseno, organtype=organtype, registrycurrency=registrycurrency, registrycapital=registrycapital,
                                    businessperiod=businessperiod, classify=classify, opendate=opendate, industryid=industryid, accountname=accountname, bankid=bankid, accountno=accountno, branchname=branchname)
            assetInfo.save()
        asset_list = Seqprocess.objects.filter(clienttype='5')
        return render(request, "data/asset/add.html", {"asset_list": asset_list})

    def asset_detail(request):
        processingno = request.GET['processingno']
        asset_detail = Seqprocess.objects.get(processingno=processingno)
        return render(request, "data/asset/detail.html", {"asset_detail": asset_detail})

    def asset_delete(request):
        if request.method == 'GET':
            processingno = request.GET['processingno']
            Seqprocess.objects.filter(processingno=processingno).delete()
            return HttpResponseRedirect("base/data/asset/")

    def readFile(filename, chunk_size=512):
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    def download_file(request):
        clienttype = request.GET['clienttype']
        processingno = request.GET['processingno']
        if clienttype == '1':
            the_file_name = toxml().read_persondata_to_xml(processingno)
        if clienttype == '2':
            the_file_name = toxml().read_organdata_to_xml(processingno)
        if clienttype == '4':
            the_file_name = toxml().read_specialoragandata_to_xml(processingno)
        if clienttype == '5':
            the_file_name = toxml().read_assetdata_to_xml(processingno)

        filename = 'E:/TestPlatform/EasyTest-master/base/result/%s' % the_file_name
        try:
            response = StreamingHttpResponse(ClientTypeData.readFile(filename))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
            return response
        except Exception:
            raise Http404

