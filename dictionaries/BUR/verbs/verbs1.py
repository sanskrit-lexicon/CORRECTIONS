# -*- coding: utf-8 -*-
"""verbs1.py for BUR
  Mar 4, 2016
 python verbs1.py ../../../orig/bur.txt ../../burhw2.txt verbs1.txt verbs1.org
"""
import re
import sys,codecs
import transcoder
transcoder.transcoder_set_dir("");

def as2slp1(x):
 y = re.sub(r'-','',x)
 z = transcoder.transcoder_processString(y,'as','slp1')
 return z

def verb1(datalines):
 """ Search for various strings in the text, and return a list of
     those strings that match
 """
 searchstrings = [  # regex
  (u'¦ *{%.*?%} *a[.] ','adj'),
  (u'¦ *{%.*?%} [mfn]+[.]','noun'),
  (u'¦.* [mfn]+[.] ','noun'),
  (u'¦.* np[.] ','proper noun'),
  (u'¦ *{%.*?%} *pp[.] ','pp'),
  (u'¦ *{%.*?%} *\(pp[.] ','pp'),
  (u'¦ *{%.*?%} *\(sup[.] ','superlative'),
  (u'¦ *{%.*?%} *inde4c[.]','indeclineable'),
  (u'¦ *{%.*?%} *interjection','interjection'),
  (u'¦ *{%.*?%} *interj[.]','interjection'),
  (u'¦ *{%.*?%} *pre4p[.] ','preposition'),
  (u'¦ *{%.*?%} *conj[.] ','conjunction'),
  (u'¦ *{%.*?%} *i[.,;]','instrumental'),
  (u'¦ *{%.*?%} *adv[.] ','adverb'),
  (u'¦ *{%.*?%} *Cf[.] ','confer'),
  (u'¦ *{%.*?%} *cf[.] ','confer'),
  (u'¦ *{%.*?%} *sup[.] ','superlative'),
  (u'¦ *{%.*?%} *compar[.] ','comparitive'),
  (u'¦ *{%.*?%} *\(?comp[.] ','comparitive'),
  (u'¦ *{%.*?%} *\(?pfx[.]','prefix'),
  (u'¦ *{%.*?%} *du[.] ','dual'),
  (u'¦ *{%.*?%} *ab[.] ','ablative'),
  (" nom[.]",'nominative'),
  ("lettre de l'alphabet",'Letter'),
  (u'¦ *{%.*?%} *\(?pf[.] ps[.] ','participle or gerund?'),
  ('idam, iyam','pronoun'),
  (' part[.] enclitique ','particle'),
  ('qui rassemble','cit suffix'),
  (u'Ami#}¦','Verb 1s'),
  (u'omi#}¦','Verb 1s'),
  (u'#mA#}¦.*adv. de ne4gation','adverb'),

  (u'¦ *{%.*?%} *impf[.] ','Verb Impf.'),
  (u'¦ *{%.*?%} +p[.] ','Verb Perfect'),
  (u'¦.* a [1-9][.]','Verb aorist'),
  (u'¦.* 3 *p[.]','Verb 3rd person'),
  (u'¦.* 2 *p[.]','Verb 2nd person'),
  (u'¦.* 1 *p[.]','Verb 1st person'),
  (u'¦.*%} +1[.,;] ','Verb class 1'),
  (u'¦.*%} +2[.,;] ','Verb class 2'),
  (u'¦.*%} +3[.,;] ','Verb class 3'),
  (u'¦.*%} +4[.,;] ','Verb class 4'),
  (u'¦.*%} +5[.,;] ','Verb class 5'),
  (u'¦.*%} +6[.,;] ','Verb class 6'),
  (u'¦.*%} +7[.,;] ','Verb class 7'),
  (u'¦.*%} +8[.,;] ','Verb class 8'),
  (u'¦.*%} +9[.,;] ','Verb class 9'),
  (u'¦.*%} +10[.,;] ','Verb class 10'),
  (u'¦ *{%.*?%} *\(?ppr[.] ','Verb pres. part.'),
  (u'¦ *{%.*?%} *ge4r[.] ','Verb gerund'),
  (u'¦ *{%.*?%} *de4s[.] ','Verb desiderative'),
  (u'¦ *{%.*?%} *de4nomin[.] ','Verb denominative'),
  (u'¦ *{%.*?%} *\(?de4n[.] ','Verb denominative'),
  (u'¦ *{%.*?%} *ps[.] ','Verb passive'),
  (u'¦ *{%.*?%} *pr[.] ','Verb present'),
  (u'¦ *{%.*?%} *imp[.] ','Verb imperative'),
  (u'¦ *{%.*?%} +o[.] ','Verb optative'),
  (u'¦ *{%.*?%} *c[.] ','Verb causative'),
  (u'¦ *{%.*?%} *aug[.] ','Verb intensive'),
  (u'¦ *{%.*?%} *pqp[.] ','Verb plus-que-parfait'),
  (u'¦ *{%.*?%} *ppf[.] ','Verb perfect participle'),
  (u'¦ *{%.*?%} *pf[.] ','Verb fut. part.'),
  (u'¦ *{%.*?%} *f ?1[.] ','Verb First Future'),
  (u'¦.* f ?1[.] ','Verb First Future'),
  (u'¦.* f ?2[.] ','Verb Second Future'),
  (u'¦ *{%.*?%} *inf[.] ','Verb Infinitive'),
  (u'¦.* aug[.]','Verb aug.'),
  (u'¦.* 1 .* 10','Verb class 1,10'),
  (u'¦.*er[ .;,]','Verb misc'),  # Particular to French text
  (u'¦ ','Verb?') # catchall

 ]
 found=[]
 #searchlines = datalines # Too many false positives
 searchlines = [datalines[0]]  # just search first line
 for (s,sp) in searchstrings:
  s1 = s
  found1=False
  for x in searchlines:
   x = re.sub(r' etc[.]','',x)
   if re.search(s1,x):
    found.append(sp)
    found1=True # so outer loop also breaks
    break  # just one classification
  if found1:
   break
 return sorted(found)

nonverbs=[
 'a', 'acala', 'acApala',
 'ajAjIva','ajakava','ajjukA','akzaDUrtila','aGos',
 'ajagava','atas','advayavAdin','an','antare','andikA','anvIta',
 'apaSada','apratyAnnAye', 'ayaTAvat','aram','arDe','alam','alpe',
 'yUyam','vayam','aha','aham','Apri','upo','ura','Urva','ekaDura',
 'ena','oM','OparoDika','ka','kadAcit','kaPavarDana','kabitTa',
 'kabila','kam','kamanIya','kara','kalp','kalpa','kA','kAwa','kAmuka',
 'kAmya','kArotara','kArya','kAlameSikA','kAlAnusArin','kiki',
 'kim','kimu','ku','kucara','kutupa','kurpAsa','kft','kftya','kfpA',
 'kfzIbala','kfzwapacya','kOlya','kzmas','Ka','ga','gama','gamya',
 'garhya','gAm','gAs','gilita',
 'araNkfta','alarzi','ale','asan','asAni','imam','IDe','udac','udanya',
 'upayozam','goBaRqIra','gosvAmin','Ga','hi','Na','ca','cana','caraT',
 'cAgaleyin','cAtaka','cire',
 'Gi' , 'cEva' , 'Ca' , 'jajYAnas',
 'jam' , 'jigfmBa' , 'jujurvas' , 'jYagiti' , 'jYawiti',
 'ta' , 'tad' , 'talina' , 'tale' , 'tava',
 'tiraSc' , 'tiras' , 'tu' , 'tuByam' , 'turya',
 'tvat' , 'tvam' , 'Ta' , 'da' , 'da',
 'darSata' , 'dASivas' , 'dilI' , 'divi' , 'dur' ,
 'dus' , 'dozin' , 'dyAm' , 'dyuzu' , 'dravya' ,
 'dva' , 'dvAnta' , 'dvAsTa' , 'dviw' , 'dveDA' ,
 'dvEmAtura' , 'Da' , 'Davala' , 'Dizwya' , 'Dfk' ,
 'na' , 'naramAninI' , 'ni' , 'nirRejaka' , 'nirDOta' ,
 'nizeDa' , 'nispanda' , 'pa' , 'parAgata' , 'pariglAna' ,
 'paricyuta' ,
 'paripUrRa' , 'parItta' , 'pareRa' , 'paryanya' , 'pAwin' ,
 'pAWa' , 'pi' , 'piNga' , 'pIta' , 'pfTivI' ,
 'pfTvI' , 'pezala' , 'pyAw' , 'prajava' , 'prajuzwa' ,
 'prajeSvara' , 'prajYa' , 'praRihita' , 'pratIcI' , 'pratIpa' ,
 'praBUta' , 'praheRaka' , 'prIRa' , 'Pa' , 'ba' ,
 'baDya' , 'balAt' , 'biBivas' , 'bodDavya' , 'Ba' ,
 'BAzya' , 'BUyas' , 'Bft' , 'mat' , 'mad' ,
 'mano' , 'mandra' , 'mama' , 'mahA' , 'mahyam' ,
 'mAm' , 'me' , 'mEvam' , 'ya' , 'yakan' ,
 'yAtnika' , 'yUTa' , 'yUn' , 'ra' , 'rAja' ,
 'rAtra' , 'roma' , 'la' , 'lakta' , 'lasta' ,
 'livi' , 'lolupa' , 'va' , 'vat' , 'vata' ,
 'vinA' , 'viniHsfta' , 'vipratisAra' , 'viprahIRa' , 'vizA' ,
 'vihA' , 'vfkza' , 'vedya' , 'vyatirikta' , 'vratati' ,
 'Sa' , 'Sakita' , 'Sakta' , 'Sakna' , 'Sakya' ,
 'SampAka' , 'SARqilya' , 'Sukam' , 'Sun' , 'SuSruvat' ,
 'Srat' , 'SrOzaw' , 'za' , 'sa' , 'sa' , 'sAye',
 'saDa' , 'santi' , 'samanvita' , 'samAsena' , 'samUlha' ,
 'samvad' , 'samvftti' , 'sudi' , 'suvyaktam' , 'sTa' ,
 'sTAtavya' , 'sma' , 'sva' , 'svit' , 'hana' ,
]
dverbs={
 'aRW':'Verb Misc',
 'az':'Verb Misc',
 'ah':'Verb Misc',
 'aMS':'Verb class 10',
 'AgaTa':'Verb form',
 'Agantu':'Verb form',
 'AYC':'Verb class 10',
 'AtatanTa':'Verb form ?',
 'Ard':'Verb Misc',
 'As':'Verb class 2',
 'iv':'Verb Misc',
 'Ij':'Verb class 1',
 'Irkzy':'Verb Misc',
 'uC':'Verb class 1,6',
 'utpadye':'Verb form',
 'utpinazmi':'Verb form',
 'upaBunajmi':'Verb form',
 'upahinasmi':'Verb form',
 'Uy':'Verb Misc.',
 'UrRu':'Verb Misc.',
 'Urd':'Verb Misc.',
 'fR':'Verb class 8',
 'ezitAsmi':'Verb form',
 'olaRq':'Verb class 10',
 'kaRq':'Verb class 10',
 'kraRW':'Verb Misc.',
 'kad':'Verb class 1',
 'kaMs':'Verb class 2',
 'kumb':'Verb class 1,10',
 'kuMS':'Verb class 1,10',
 'kur':'Verb Misc.',
 'kUq':'Verb class 6',
 'kfp':'Verb class 1',
 'kfz':'Verb class 1,6',
 'kF':'Verb class 5,9',
 'ket':'Verb class 10',
 'knaT':'Verb Misc.',
 'knaMs':'Verb class 10',
 'knu':'Verb Misc.',
 'kraT':'Verb class 1,10',
 'krad':'Verb Misc.',
 'krIl':'Verb Misc.',
 'klad':'Verb class 1',
 'klind':'Verb class 1',
 'klIb':'Verb class 1',
 'kzaj':'Verb class 1,10',
 'kzamp':'Verb class 1,10',
 'KAd':'Verb class 1',
 'Kuj':'Verb class 1',
 'KuRq':'Verb class 1,10',
 'KyA':'Verb Misc.',
 'gaRq':'Verb Misc.',
 'garh':'Verb Misc.',
 'gA':'Verb Misc.',
 'guRq':'Verb class 1,10',
 'gup':'Verb class 10',
 'guP':'Verb Misc.',
 'gurd':'Verb class 1,10',
 'gf':'Verb Misc.',
 'gfB':'Verb Misc.',
 'gfmB':'Verb Misc.',
 'gfh':'Verb Misc.',
 'graT':'Verb class 1,9',
 'graB':'Verb Misc.',
 'gras':'Verb class 1,10',
 'Gaww':'Verb class 1,10',
 'GaRw':'Verb class 1,10',
 'Gamb':'Verb Misc.',
 'GaMz':'Verb Misc.',
 'GUrR':'Verb class 1,6',
 'Gf':'Verb Misc.',
 'GrA':'Verb class 1,2',
 'caNkramye':'Verb form',
 'caYcUrye':'Verb form',
 'caw':'Verb class 1,10',
 'caR':'Verb class 10',
 'caRq':'Verb class 1,10',
 'carIkfzye':'Verb form intensive',
 'carc':'Verb class 1,6',
 'carv':'Verb class 1,10',
 'cal':'Verb Misc.',
 'calIkalpye':'Verb form intensive',
 'ciw':'Verb class 1,10',
 'citrIye':'Verb form denominative',
 #
 'GaMs':'Verb class 1',
 'cIk':'Verb class 1,10',
 'cuw':'Verb class 6,10',
 'cuRw':'Verb class 1',
 'cuRw':'Verb class 10',
 'cub':'Verb class 1,10',
 'cfp':'Verb class 1,10',
 'Cad':'Verb Misc',
 'Cand':'Verb class 1,10',
 'Cuw':'Verb class 1,10',
 'Cfd':'Verb class 1,10',
 'Cfp':'Verb class 1,10',
 'Co':'Verb class 4',
 'jaNGanmi':'Verb aug',
 'jaj':'Verb Misc',
 'jaB':'Verb class 1',
 'jaB':'Verb class 10',
 'jariharmi':'Verb aug',
 'jarc':'Verb class 1,6',
 'jarj':'Verb Misc',
 'jal':'Verb class 1,10',
 'jaMs':'Verb class 1,10',
 'jAgAhmi':'Verb aug',
 'jAgf':'Verb Misc',
 'jAhasmi':'Verb aug',
 'jIyAsam':'Verb aorist',
 'juz':'Verb class 6,1',
 'jfB':'Verb class 1',
 'jF':'Verb Misc',
 'jeGemi':'Verb aug',
 'jeGnIye':'Verb aug',
 'jejayImi':'Verb aug',
 'jejremi':'Verb aug',
 'jeya':'Verb form',
 'jehremi':'Verb aug',
 'jogohmi':'Verb form',
 'jri':'Verb class 1,9,10',
 'JF':'Verb class 4,9',
 'waNk':'Verb class 10,1',
 'qap':'Verb class 10',
 'qamB':'Verb Misc',
 'taMs':'Verb class 1,10',
 'tAtabmi':'Verb aug',
 'tAye':'Verb class 1',
 'tArizam':'Verb form',
 'titikze':'Verb desid',
 'tirodaDe':'Verb Misc',
 'tuj':'Verb class 1,6',
 'tutT':'Verb class 10',
 'tumb':'Verb class 1,10',
 'tfpAye':'Verb denom',
 'tfptAye':'Verb denom',
 'traMs':'Verb class 1,10',
 'trE':'Verb class 1',
 'TuD':'Verb class 4',
 'dakz':'Verb Misc',
 'daG':'Verb class 4',
 'dad':'Verb form',
 'dandahmi':'Verb aug',
 'daB':'Verb class 1,10',
 'didAse':'Verb desid',
 'dih':'Verb class 2',
 'dIDI':'Verb class 2',
 'dIp':'Verb class 4',
 'durmanAye':'Verb denom',
 'duHK':'Verb class 4,10',
 'duh':'Verb class 2',
 'dfS':'Verb class 1',
 'dF':'Verb class 1,9',
 'deya':'Verb perfect',
 'drA':'Verb class 2',
 'drE':'Verb class 2,4',
 'Dan':'Verb Misc',
 'DU':'Verb class 5,9,6,1',
 'DUp':'Verb denom',
 'DUS':'Verb class 10',
 'Dfj':'Verb class 1',
 'DyE':'Verb class 1',
 'Dras':'Verb Misc',
 'DvaMs':'Verb Misc',
 'naD':'Verb Misc',
 'nigUhe':'Verb Misc',
 'nijAgarmi':'Verb aug',
 'nidIDye':'Verb Misc',
 'nibADe':'Verb Misc',
 'niBanajma':'Verb Misc',
 'nimArjmi':'Verb Misc',
 'niyunajmi':'Verb Misc',
 'niyOmi':'Verb Misc',
 'niriRye':'Verb Misc',
 'niremi':'Verb Misc',
 'nirodaDe':'Verb form',
 'nirgE':'Verb Misc',
 'nirRaye':'Verb Misc',
 'nirdohmi':'Verb Misc',
 'nirBImi':'Verb Misc',
 'nirBinadmi':'Verb Misc',
 'nirvarte':'Verb Misc',
 'nirvidye':'Verb Misc',
 'nirvfRajmi':'Verb Misc',
 'nirhanmi':'Verb Misc',
 'nirhrase':'Verb Misc',
 'nilIye':'Verb Misc',
 'nivAsaye':'Verb caus.',
 'niviSe':'Verb Misc',
 'nivedmi':'Verb Misc',
 'niSIye':'Verb Misc',
 'niSvasimi':'Verb Misc',
 'nizaje':'Verb Misc',
 'nizeve':'Verb Misc',
 'nizkASe':'Verb Misc',
 'nizpadye':'Verb Misc',
 'nizpinazmi':'Verb Misc',
 'nizpipami':'Verb Misc',
 'nizvapimi':'Verb Misc',
 'nistOmi':'Verb Misc',
 'niHSAsmi':'Verb Misc',
 'niHSvasimi':'Verb Misc',
 'nihanmi':'Verb Misc',
 'nihIye':'Verb Misc',
 'nihnuve':'Verb Misc',
 'nihfvaye':'Verb Misc',
 'nft':'Verb class 4',
 'nyasmi':'Verb form',
 'nyUhe':'Verb Misc',
 'nyfYje':'Verb Misc',
 'pac':'Verb Misc',
 'paw':'Verb class 10',
 'pan':'Verb class 10,1',
 'parAvarte':'Verb Misc',
 'parAvfRajmi':'Verb Misc',
 'parASvasimi':'Verb Misc',
 'parAhanmi':'Verb Misc',
 'parikalpayami':'Verb Misc',
 'parikrIqe':'Verb Misc',
 'parikrIRe':'Verb Misc',
 'parikzIye':'Verb Misc',
 'pariKaRqe':'Verb Misc',
 'parigarhe':'Verb Misc',
 'paricakze':'Verb Misc',
 'pariCinadmi':'Verb Misc',
 'pariRihanmi':'Verb Misc',
 'paritapye':'Verb Misc',
 'paritrAye':'Verb Misc',
 'paridUye':'Verb Misc',
 'parideve':'Verb Misc',
 'pariveda':'Verb Perfect',
 'paSya':'Verb imperative',
 'plI':'Verb class 9',
 'plu':'Verb class 1',
 'pluz':'Verb class 1,4',
 'brU':'Verb class 2',
 'Brej':'Verb class 1,10',
 'yas':'Verb class 1,6',
 'yOq':'Verb Misc',
 'lih':'Verb class 2,1',
 'paridehmi':'Verb Misc',
 'pariBraSaye':'Verb Misc',
 'parimarmfjye':'Verb Misc',
 'pariyate':'Verb Misc',
 'parilupye':'Verb Misc',
 'parivarDe':'Verb Misc',
 'pariviSvasimi':'Verb Misc',
 'parivezwe':'Verb Misc',
 'pariSIrye':'Verb Misc',
 'parizeve':'Verb Misc',
 'parizvaje':'Verb Misc',
 'parihIye':'Verb Misc',
 'parRa':'Verb Misc',
 'paryavatizWe':'Verb Misc',
 'paryasmi':'Verb Misc',
 'paryavarte':'Verb Misc',
 'paryAse':'Verb Misc',
 'paryudvinajmi':'Verb Misc',
 'paryupAse':'Verb Misc',
 'palAye':'Verb Misc',
 'palyemi':'Verb Misc',
 'pArzada':'Verb Misc',
 'pAl':'Verb Misc',
 'pinahye':'Verb Misc',
 'pipatizat':'Verb Misc',
 'piz':'Verb Misc',
 'pI':'Verb Misc',
 'pUrv':'Verb Misc',
 'pE':'Verb Misc',
 'prakzIye':'Verb Misc',
 'praRidehmi':'Verb Misc',
 'pratijare':'Verb Misc',
 'pratijuze':'Verb Misc',
 'pratidozayAti':'Verb Misc',
 'pratinivarte':'Verb Misc',
 'pratibravImi':'Verb Misc',
 'pratiBAze':'Verb Misc',
 'pratimode':'Verb Misc',
 'pratiyuDye':'Verb Misc',
 'prativacmi':'Verb Misc',
 'prativijAne':'Verb Misc',
 'prativedmi':'Verb Misc',
 'pratisaYjAye':'Verb Misc',
 'pratisamucye':'Verb Misc',
 'pratisamboDe':'Verb Misc',
 'pratihanmi':'Verb Misc',
 'pratyaDyemi':'Verb Misc',
 'pratyanutapye':'Verb Misc',
 'pratyavatizWe':'Verb Misc',
 'pratyupapadye':'Verb Misc',
 'pradIdye':'Verb Misc',
 'pradvezmi':'Verb Misc',
 'praDvaMsayAti':'Verb Misc',
 'praparAye':'Verb Misc',
 'praplave':'Verb Misc',
 'prabiBemi':'Verb Misc',
 'prabravImi':'Verb Misc',
 'praBraSye':'Verb Misc',
 'prayuYje':'Verb Misc',
 'prayuyutse':'Verb Misc',
 'pralIye':'Verb Misc',
 'pralupye':'Verb Misc',
 'pravarDe':'Verb Misc',
 'pravase':'Verb Misc',
 'pravilIye':'Verb Misc',
 'pravevedmi':'Verb Misc',
 'pravezwe':'Verb Misc',
 'pravyaTe':'Verb Misc',
 'prasajye':'Verb Misc',
 'prasiYcye':'Verb Misc',
 'prasIdAmiM':'Verb Misc',
 'prasvapimi':'Verb Misc',
 'prAyuDye':'Verb Misc',
 'prAraBe':'Verb Misc',
 'prAsmi':'Verb Misc',
 'prAha':'Verb Misc',
 'prI':'Verb Misc',
 'prIyAye':'Verb Misc',
 'prekze':'Verb Misc',
 'preyarmi':'Verb Misc',
 'pro':'Verb Misc',
 'protsahe':'Verb Misc',
 'prorROmi':'Verb Misc',
 'banD':'Verb Misc',
 'bahl':'Verb Misc',
 'bIBatse':'Verb Misc',
 'boBojmi':'Verb Misc',
 'Bakz':'Verb Misc',
 'BaYj':'Verb Misc',
 'Barts':'Verb Misc',
 'Bikz':'Verb Misc',
 'BIzaye':'Verb Misc',
 'Buj':'Verb Misc',
 'BUz':'Verb Misc',
 'Bram':'Verb Misc',
 'BraMS':'Verb Misc',
 'maYj':'Verb Misc',
 'maT':'Verb Misc',
 'man':'Verb Misc',
 'mamre':'Verb Misc',
 'mAh':'Verb Misc',
 'mI':'Verb Misc',
 'mfkz':'Verb Misc',
 'mfg':'Verb Misc',
 'mfj':'Verb Misc',
 'mfl':'Verb Misc',
 'mruc':'Verb Misc',
 'mrew':'Verb Misc',
 'mlakz':'Verb Misc',
 'mlew':'Verb Misc',
 'yuyutse':'Verb Misc',
 'ramB':'Verb Misc',
 'ramrammi':'Verb Misc',
 'riraMse':'Verb Misc',
 'rih':'Verb Misc',
 'laq':'Verb Misc',
 'laq':'Verb Misc',
 'laRq':'Verb Misc',
 'lalat':'Verb Misc',
 'lalantI':'Verb Misc',
 'laz':'Verb Misc',
 'luW':'Verb Misc',
 'leK':'Verb Misc',
 'lolupye':'Verb Misc',
 'vaK':'Verb Misc',
 'vac':'Verb Misc',
 'vaYc':'Verb Misc',
 'vaRq':'Verb Misc',
 'van':'Verb Misc',
 'vam':'Verb Misc',
 'vAYC':'Verb Misc',
 'vAvasmi':'Verb Misc',
 'vAvftye':'Verb Misc',
 'vAS':'Verb Misc',
 'vikawWe':'Verb Misc',
 'vikrIRe':'Verb Misc',
 'vicikite':'Verb Misc',
 'vicezwe':'Verb Misc',
 'viC':'Verb Misc',
 'vijaye':'Verb Misc',
 'vijugupse':'Verb Misc',
 'vidvize':'Verb Misc',
 'viD':'Verb Misc',
 'vinande':'Verb Misc',
 'viniyunajmi':'Verb Misc',
 'vipadye':'Verb Misc',
 'vipratipadye':'Verb Misc',
 'vipraTe':'Verb Misc',
 'viprayunajmi':'Verb Misc',
 'viplave':'Verb Misc',
 'vibAbaDye':'Verb Misc',
 'viBAse':'Verb Misc',
 'viByase':'Verb Misc',
 'viruDye':'Verb Misc',
 'vilajje':'Verb Misc',
 'vilIye':'Verb Misc',
 'vivarDe':'Verb Misc',
 'vivase':'Verb Misc',
 'viSIrye':'Verb Misc',
 'viSrUye':'Verb Misc',
 'vihanmi':'Verb Misc',
 'vI':'Verb Misc',
 'vf':'Verb Misc',
 'vfz':'Verb Misc',
 'vfMh':'Verb Misc',
 'vF':'Verb Misc',
 'vetTa':'Verb Misc',
 'vezw':'Verb Misc',
 'vyatilUne':'Verb Misc',
 'vyaSnave':'Verb Misc',
 'vyAGUrRe':'Verb Misc',
 'vyApriye':'Verb Misc',
 'vrIs':'Verb Misc',
 'vlekz':'Verb Misc',
 'Sad':'Verb Misc',
 'Sap':'Verb Misc',
 'SaMs':'Verb Misc',
 'SASaMsmi':'Verb Misc',
 'SASvasmi':'Verb Misc',
 'SiYj':'Verb Misc',
 'SiSayize':'Verb Misc',
 'Suc':'Verb Misc',
 'SuRW':'Verb Misc',
 'SuSrUze':'Verb Misc',
 'Sf':'Verb Misc',
 'SoSucye':'Verb Misc',
 'SvaW':'Verb Misc',
 'Sval':'Verb Misc',
 'zWiv':'Verb Misc',
 'zvakk':'Verb Misc',
 'saNkIrye':'Verb Misc',
 'saNkzIye':'Verb Misc',
 'sac':'Verb Misc',
 'saYcakze':'Verb Misc',
 'saYcezwe':'Verb Misc',
 'saYjAye':'Verb Misc',
 'sad':'Verb Misc',
 'sanniyuYje':'Verb Misc',
 'sannivarte':'Verb Misc',
 'samaYce':'Verb Misc',
 'samaDyAse':'Verb Misc',
 'samaDyemi':'Verb Misc',
 'samanujAye':'Verb Misc',
 'samanuvarte':'Verb Misc',
 'samapaDyAye':'Verb Misc',
 'samaBijAye':'Verb Misc',
 'samaBipadye':'Verb Misc',
 'samaByupemi':'Verb Misc',
 'samaSnave':'Verb Misc',
 'samAdade':'Verb Misc',
 'samApyAye':'Verb Misc',
 'samAyate':'Verb Misc',
 'samASvasimi':'Verb Misc',
 'saminDe':'Verb Misc',
 'samucCinadmi':'Verb Misc',
 'samutpadye':'Verb Misc',
 'samupajAye':'Verb Misc',
 'samupatapye':'Verb Misc',
 'samupayunajmi':'Verb Misc',
 'samupaseve':'Verb Misc',
 'samupAdade':'Verb Misc',
 'samupAse':'Verb Misc',
 'samupekze':'Verb Misc',
 'samfYje':'Verb Misc',
 'sameDe':'Verb Misc',
 'samEmi':'Verb Misc',
 'samparyemi':'Verb Misc',
 'sampalAye':'Verb Misc',
 'sampratIkze':'Verb Misc',
 'sampratyAcakze':'Verb Misc',
 'sampratyemi':'Verb Misc',
 'sampradfSye':'Verb Misc',
 'samprapadye':'Verb Misc',
 'samprayunajmi':'Verb Misc',
 'sampralIye':'Verb Misc',
 'sampravyaTe':'Verb Misc',
 'sampriye':'Verb Misc',
 'sambuDye':'Verb Misc',
 'samBARqaye':'Verb Misc',
 'sammantraye':'Verb Misc',
 'samyuDye':'Verb Misc',
 'samyunajmi':'Verb Misc',
 'samyOmi':'Verb Misc',
 'samrame':'Verb Misc',
 'samlajje':'Verb Misc',
 'samvarte':'Verb Misc',
 'samvarDe':'Verb Misc',
 'samvalita':'Verb Misc',
 'samvinde':'Verb Misc',
 'samvivarDe':'Verb Misc',
 'saMSyAye':'Verb Misc',
 'saMsismaye':'Verb Misc',
 'sAD':'Verb Misc',
 'sAsadmi':'Verb Misc',
 'sAsahmi':'Verb Misc',
 'si':'Verb Misc',
 'siD':'Verb Misc',
 'siB':'Verb Misc',
 'susmUrze':'Verb Misc',
 'sUyava':'Verb Misc',
 'so':'Verb Misc',
 'skumB':'Verb Misc',
 'stumB':'Verb Misc',
 'stUp':'Verb Misc',
 'stf':'Verb Misc',
 'sPuRq':'Verb Misc',
 'svan':'Verb Misc',
 'svask':'Verb Misc',
 'hf':'Verb Misc',
 'hve':'Verb Misc',
}
def disp_org(icase,wordtype,hw0,url,page0,datalines):
 """ return array of lines, formatted for details of Emacs org mode
 """
 outarr=[]
 pageref = "[[%s][page %s]]" %(url,page0)
 outarr.append('* Case %04d: %s %s %s ' % (icase, wordtype,hw0,pageref))
  # output up to 10 lines of datalines
 outlines = datalines[0:10]
 for x in outlines:
  # Remove '|', which is a line-separator in BUR
  x = re.sub(r'[|]','',x)
  y = transcoder.transcoder_processString(x,'as','roman')
  outarr.append(';  %s' % y)
 if len(datalines)>10:
  ndiff = len(datalines) - 10
  outarr.append(';   [and %s more lines]' % ndiff)
 outarr.append('')
 return outarr

def disp_md(icase,wordtype,hw0,url,page0,datalines):
 """ return array of lines, formatted for details of GitHub Markdown
 """
 outarr=[]
 pageref = "[page %s](%s)" %(page0,url)
 outarr.append(' Case %04d: %s **%s** %s ' % (icase, wordtype,hw0,pageref))
  # output up to 10 lines of datalines
 outlines = datalines[0:10]
 outarr.append('```')
 for x in outlines:
  # Remove '|', which is a line-separator in BUR
  x = re.sub(r'[|]','',x)
  y = transcoder.transcoder_processString(x,'as','roman')
  if (y.strip() != ''):
   outarr.append('%s' % y)
 if len(datalines)>10:
  ndiff = len(datalines) - 10
  outarr.append('  [and %s more lines]' % ndiff)
 outarr.append('```')
 outarr.append('------------------------------------------')
 outarr.append('')
 return outarr

def main(inlines,hwrecs,fileout,fileout1,fileouta,fileout1a,fileout2,fileout2a):
 fout=codecs.open(fileout,"w","utf-8")
 fout1=codecs.open(fileout1,"w","utf-8")
 fouta=codecs.open(fileouta,"w","utf-8")
 fout1a=codecs.open(fileout1a,"w","utf-8")
 fout2=codecs.open(fileout2,"w","utf-8")
 fout2a=codecs.open(fileout2a,"w","utf-8")
 nsystematic=0
 nout=0
 nouta=0
 for hwrec in hwrecs:
  datalines = inlines[hwrec.linenum1-1:hwrec.linenum2]
  # is it a foreign word? If so, get list of languages.
  hw0 = hwrec.hwslp
  L = hwrec.lnum
  if hw0 in dverbs:
   fw=[dverbs[hw0]]
  else:
   fw = verb1(datalines) 
   if len(fw) == 0:  # len(fw) is always 1
    continue
  wordtype=fw[0] # in this case, len(fw) = 1
  # skip some
  if not wordtype.startswith('Verb'):
   continue
  # for dev, just print the Verb? cases
  #if not wordtype.startswith('Verb?'):
  # continue
  firstline = datalines[0] 
  page0 = hwrec.pagecol
  l1 = hwrec.linenum1
  l2 = hwrec.linenum2
  if hw0 in nonverbs:
   continue
  # decide which output this case goes to
  # (a) a 'simple root' or
  # (b) a 'verb form'
  # decide this on basis of 'hw0'
  # In almost all cases, (a) occurs when there is only one vowel in hw0.
  m = re.findall(r'[aAiIuUfFxXeEoO]',hw0)
  if (len(m) == 1) or (hw0=='UrRu'):
   (wordtype,f,f1,f2) = ('Root',fout,fout1,fout2)
   nout = nout+1
   icase = nout
  else:
   (wordtype,f,f1,f2) = ('Verb form',fouta,fout1a,fout2a)
   nouta = nouta + 1
   icase = nouta
  dictcode='bur'
  # output to fileout
  #out = "%s:%s: %s" %(dictcode,hw0,','.join(fw))
  out = "%s:%s,%s: %s" %(dictcode,hw0,L,wordtype)
  f.write("%s\n" % out)
  # output to Org mode and Markdown
  baseurl='http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=%s'% dictcode
  url = '%s&page=%s' %(baseurl,page0)
  # org mode
  outarr = disp_org(icase,wordtype,hw0,url,page0,datalines)
  f1.write('\n'.join(outarr))
  # markdown
  outarr = disp_md(icase,wordtype,hw0,url,page0,datalines)
  f2.write('\n'.join(outarr))
  if ((nout+nouta) == 100) and False:  # dbg
   print "debug",icase
   break
   pass
 fout.close()
 fout1.close()
 fouta.close()
 fout1a.close()
 print len(hwrecs),"headword records processed"
 print nout,"records written to ",fileout
 print nout,"sections written to ",fileout1
 print nouta,"records written to ",fileouta
 print nouta,"sections written to ",fileout1a

 
class Headword(object):
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.line = line
  self.lnum = n
  (self.pagecol,self.hwslp,linenum12) = re.split('[:]',line)
  (linenum1,linenum2) = re.split(r',',linenum12)
  self.linenum1=int(linenum1)
  self.linenum2=int(linenum2)

def init_headwords(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = []
  lnum=0
  for x in f:
   lnum = lnum+1
   recs.append(Headword(x,lnum))
 return recs

if __name__ == "__main__":
 filein=sys.argv[1] #  X.txt
 filein1=sys.argv[2] # Xhw2.txt
 fileout =sys.argv[3] #  
 fileout1 =sys.argv[4] #  Emacs Ord Mode listing
 fileouta =sys.argv[5] #  
 fileout1a =sys.argv[6] #  Emacs Ord Mode listing
 fileout2 = sys.argv[7] # Markdown listing
 fileout2a = sys.argv[8] # Markdown listing

 # slurp X.txt file into list of lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  inlines = [x.rstrip('\r\n') for x in f]
 # construct headword records
 hwrecs=init_headwords(filein1)
 main(inlines,hwrecs,fileout,fileout1,fileouta,fileout1a,fileout2,fileout2a)
