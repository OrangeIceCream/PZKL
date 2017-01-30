#!/usr/bin/env python3

# Импортируем структуры
from freparser.tokens import TokensStorage
from freparser.spans import SpansStorage
from freparser.objects import ObjectsStorage
from freparser.corefs import CorefsStorage
from freparser.facts import FactsStorage
from subprocess import call
import json
import codecs
from xml.dom import minidom
from shutil import copyfile

filenumbers=[58,61,74,93,98,99,100,105,115,117,124,127,129,131,142,145,146,147,151,154,156,176,179,180,182,188,189,191,193,194,\
			215,228,247,252,253,256,258,259,260,261,263,270,271,278,282,286,288,290,294,295,296,297,301,302,310,314,317,323,324,\
			326,333,335,336,337,344,346,347,348,349,354,356,361,365,367,369,370,374,375,383,389,392,394,396,397,398,399,401,402,\
			409,410,411,412,413,424,425,426,434,438,443,444,448,455,457,461,462,475,480,483,489,498,503,504,506,510,542,546,618,\
			622,737,1256,1667,3269]

testfilenumbers=[3539,3543,3555,3562,3573,3574,3581,3591,3602,3615,3626,3632,3644,3647,3667,3677,3680,3687,3688,3696,3697,3700,\
				3702,3708,3714,3716,3725,3734,3744,3746,3752,3756,3757,3758,3760,3762,3763,3764,3765,3767,3768,3769,3770,3771,\
				3772,3773,3774,3775,3776,3779,3780,3790,3791,3792,3793,3794,3795,3796,3797,3798,3799,3800,3801,3802,3804,3805,\
				3806,3808,3809,3810,3811,3812,3817,3820,3824,3828,3829,3832,3833,3840,3842,3860,3865,3872,3876,3877,3878,3880,\
				3881,3882,3883,3884,3885,3886,3887,3888,3889,3890,3894,3902,3904,3909,3910,3915,3916,3920,3927,3928,3937,3938,\
				3940,3942,3944,3946,3954,3961,3962,3965,3966,3971,3972,3973,3974,3975,3976,3977,3978,3979,3980,3981,3982,3983]

def get_obj_text(object_id):
	obj = objects[object_id]
	obj_spans = obj.related_spans
	obj_text = ""
	obj_tokens_set = set();
	for span in obj_spans:
		span_tokens = span.tokens
		for token in span_tokens:
			obj_tokens_set.add(token.id)
	obj_tokens_set = list(obj_tokens_set)
	obj_tokens_set.sort()
	for token_id in obj_tokens_set:
		obj_text += " " + tokens[token_id].text
	obj_text = obj_text[1:] 
	
	mystem_file = codecs.open("mystem_file.txt","w",encoding="utf-8")
	mystem_file.write(obj_text)
	mystem_file.close()
	call(["mystem.exe","mystem_file.txt","mystem_file_out.txt","-l","--format","json","-d"])
	mystem_file_out = codecs.open("mystem_file_out.txt","r",encoding="utf-8")
	lemmas = json.loads(mystem_file_out.readline())
	mystem_file_out.close()
	lemmas_text = ""
	for lemma in lemmas:
		if lemma["analysis"] != []:
			lemmas_text += ' "'+lemma["analysis"][0]["lex"]+'"'
		else:
			lemmas_text += ' "'+lemma["text"]+'"'
	return lemmas_text

def get_span_text(span_id):
	span = spans[span_id]
	span_text = ""
	span_tokens_set = set()
	for token in span.tokens:
		span_tokens_set.add(token.id)
	span_tokens_set = list(span_tokens_set)
	span_tokens_set.sort()
	for token_id in span_tokens_set:
		span_text += " " + tokens[token_id].text
	span_text = span_text[1:]

	mystem_file = codecs.open("mystem_file.txt","w",encoding="utf-8")
	mystem_file.write(span_text)
	mystem_file.close()
	call(["mystem.exe","mystem_file.txt","mystem_file_out.txt","-l","--format","json","-d"])
	mystem_file_out = codecs.open("mystem_file_out.txt","r",encoding="utf-8")
	lemmas = json.loads(mystem_file_out.readline())
	mystem_file_out.close()
	lemmas_text = ""
	for lemma in lemmas:
		if lemma["analysis"] != []:
			lemmas_text += ' "'+lemma["analysis"][0]["lex"]+'"'
		else:
			lemmas_text += ' "'+lemma["text"]+'"'
	return lemmas_text

def build_person_grammar():
	grammar_file = open("PersonGrammar.cxx","w",encoding="utf-8")
	grammar_file.write('#encoding "utf-8"\n'+'#GRAMMAR_ROOT Person\n\n')
	count=0

	person_objects = objects.list_by_type("Person")
	for obj in person_objects:
		text = get_obj_text(obj.id)
		if text!="": 
			grammar_file.write('Person -> '+ text +';\n')
			count+=1
	
	grammar_file.close()
	return count

def build_org_grammar():
	grammar_file = open("OrgGrammar.cxx","w",encoding="utf-8")
	grammar_file.write('#encoding "utf-8"\n'+'#GRAMMAR_ROOT Org\n\n')
	count=0
	
	org_objects = objects.list_by_type("Org")
	for obj in org_objects:
		text = get_obj_text(obj.id)
		if text!="": 
			grammar_file.write('Org -> '+ text +';\n')
			count+=1

	org_objects = objects.list_by_type("LocOrg")
	for obj in org_objects:
		text = get_obj_text(obj.id)
		if text!="": 
			grammar_file.write('Org -> '+ text +';\n')
			count+=1
	
	grammar_file.close()
	return count

def build_job_grammar():
	grammar_file = open("JobGrammar.cxx","w",encoding="utf-8")
	grammar_file.write('#encoding "utf-8"\n'+'#GRAMMAR_ROOT Org\n\n')	
	count=0

	job_spans = spans.list_by_type("job")
	for span in job_spans:
		text = get_span_text(span.id)
		if text!="": 
			grammar_file.write('Job -> '+ text +';\n')
			count+=1

	grammar_file.close()
	return count

def build_fact_grammar():
	print("start person")
	person_count=build_person_grammar()
	print("finish person")
	print("start org")
	org_count=build_org_grammar()
	print("finish org")
	print("start job")
	job_count=build_job_grammar()
	print("finish job")

	if(person_count==0 or job_count==0):
		return False
	else:
		grammar_file = open("FactGrammar.cxx","w",encoding="utf-8")
		grammar_file.write('#encoding "utf-8"\n#include <OrgGrammar.cxx>\n#include <PersonGrammar.cxx>\n#include <JobGrammar.cxx>\n#GRAMMAR_ROOT F\n\n')
		grammar_file.write('F -> Job interp (Occupation.Job::not_norm) Person interp (Occupation.Person::not_norm);\n')
		if(org_count!=0):
			grammar_file.write('F -> Job interp (Occupation.Job::not_norm) Org interp (Occupation.Org::not_norm) Person interp (Occupation.Person::not_norm);\n')
			grammar_file.write('F -> Job interp (Occupation.Job::not_norm) Org interp (Occupation.Org::not_norm) Word Person interp (Occupation.Person::not_norm);\n')
			grammar_file.write('F -> Job interp (Occupation.Job::not_norm) Org interp (Occupation.Org::not_norm) Word Word Person interp (Occupation.Person::not_norm);\n')
			grammar_file.write('F -> Job interp (Occupation.Job::not_norm) Org interp (Occupation.Org::not_norm) Word Word Word Person interp (Occupation.Person::not_norm);\n')
			grammar_file.write('F -> Person interp (Occupation.Person::not_norm) Job interp (Occupation.Job::not_norm) Org interp (Occupation.Org::not_norm);\n')		
			grammar_file.write('F -> Person interp (Occupation.Person::not_norm) Job interp (Occupation.Job::not_norm) Word Org interp (Occupation.Org::not_norm);\n')
			grammar_file.write('F -> Person interp (Occupation.Person::not_norm) Job interp (Occupation.Job::not_norm) Word Word Org interp (Occupation.Org::not_norm);\n')
			grammar_file.write('F -> Job interp (Occupation.Job::not_norm) Word Org interp (Occupation.Org::not_norm) Person interp (Occupation.Person::not_norm);\n')
			grammar_file.write('F -> Job interp (Occupation.Job::not_norm) Word Word Org interp (Occupation.Org::not_norm) Person interp (Occupation.Person::not_norm);\n')
			grammar_file.write('F -> Job interp (Occupation.Job::not_norm) Word Word Word Org interp (Occupation.Org::not_norm) Person interp (Occupation.Person::not_norm);\n')
		grammar_file.close()
		return True

def parse_xml(output_file):
	xml_doc = minidom.parse("CurrentOutput.xml")
	occupation_facts = xml_doc.getElementsByTagName('Occupation')
	for fact in occupation_facts:
		output_file.write("Occupation\n")
		person = fact.getElementsByTagName("Person")
		output_file.write("who:"+person[0].getAttribute('val').lower()+"\n")
		org = fact.getElementsByTagName("Org")
		if org: output_file.write("where:"+org[0].getAttribute('val').lower()+"\n")
		job = fact.getElementsByTagName("Job")
		if job: output_file.write("job:"+job[0].getAttribute('val').lower()+"\n\n")

prefix = None
tokens = None
spans = None
objects = None
corefs = None
facts = None

for num in testfilenumbers:
	print(num)
	prefix = "./RuEval/testset/book_"+str(num)
	tokens = TokensStorage.load_from_file("{}.tokens".format(prefix))
	spans = SpansStorage.load_from_file("{}.spans".format(prefix), tokens)
	objects = ObjectsStorage.load_from_file("{}.objects".format(prefix), spans)
	corefs = CorefsStorage.load_from_file("{}.coref".format(prefix), objects)
	facts = FactsStorage.load_from_file("{}.facts".format(prefix))
	
	copyfile(prefix+".txt", "CurrentBook.txt")
	
	f=open("CurrentOutput.xml","w")
	f.close()
	output_file = open(prefix+".task3","w",encoding="utf-8")

	if(build_fact_grammar()):
		call(["tomitaparser.exe","config.proto"])
		parse_xml(output_file)
	
	output_file.close()




