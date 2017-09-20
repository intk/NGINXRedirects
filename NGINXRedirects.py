# -*- coding: utf-8 -*-

TEMPLATE = 'location ~ ^%s {\n\trewrite ^ %s? permanent;\n}\n'
TEMPLATEARGS =  'location ~ ^%s {%s}\n'
TEMPLATEINNER = "\n\tif ($args ~ %s) {\n\t\trewrite ^ %s? permanent;\n\t}\n"


redirects = [
	('/tentoonstelling.php','http://www.kunsthalkade.nl/nl/nu-en-verwacht/tentoonstellingen'),
	('/over.php?item=51','http://www.kunsthalkade.nl/nl/plan-je-bezoek/praktische-informatie'),
	('/index.php','/http://www.kunsthalkade.nl/nl/'),
	('/tentoonstelling.php?item=3073','http://www.kunsthalkade.nl/nl/tentoonstellingen/de-kleuren-van-de-stijl'),
	('/over.php','http://www.kunsthalkade.nl/nl/over-kade'),
	('/cafe.php','http://www.kunsthalkade.nl/nl/plan-je-bezoek/kadecafe'),
	('/tentoonstelling.php?item=3073&offset=0','http://www.kunsthalkade.nl/nl/tentoonstellingen/de-kleuren-van-de-stijl'),
	('/tentoonstelling.php?item=3072','http://www.kunsthalkade.nl/nl/tentoonstellingen/goed-gemaakt-ode-aan-het-maakproces'),
	('/agenda.php','http://www.kunsthalkade.nl/nl/nu-en-verwacht'),
	('/tentoonstelling.php?item=2965','http://www.kunsthalkade.nl/nl/tentoonstellingen/self-fiction-dubbelsolo-david-altmejd-friedrich-kunath'),
	('/shop.php','http://www.kunsthalkade.nl/nl/plan-je-bezoek/kadeshop'),
	('/over.php?item=91','http://www.kunsthalkade.nl/nl/plan-je-bezoek/praktische-informatie'),
	('/tentoonstelling.php?item=3072&offset=0','http://www.kunsthalkade.nl/nl/tentoonstellingen/goed-gemaakt-ode-aan-het-maakproces'),
	('/agendaItem.php?item=3134&periode=&genre=','http://www.kunsthalkade.nl/nl/nu-en-verwacht'),
	('/over.php?item=54','http://www.kunsthalkade.nl/nl/over-kade/contact'),
	('/tentoonstelling.php?item=2515&offset=0','http://www.kunsthalkade.nl/nl/online-archief'),
	('/rondleidingen.php','http://www.kunsthalkade.nl/nl/over-kade'),
	('/educatie.php','http://www.kunsthalkade.nl/nl/over-kade'),
	('/tentoonstelling.php?item=2965&offset=0','http://www.kunsthalkade.nl/nl/tentoonstellingen/self-fiction-dubbelsolo-david-altmejd-friedrich-kunath'),
	('/beeldbank.php','http://www.kunsthalkade.nl/nl/online-archief'),
	('/tentoonstelling.php?item=3191&offset=0','http://www.kunsthalkade.nl/nl/tentoonstellingen/vuur'),
	('/tentoonstelling.php?item=680','http://www.kunsthalkade.nl/nl/tentoonstellingen/shadowdance'),
	('/tentoonstelling.php?item=3191','http://www.kunsthalkade.nl/nl/tentoonstellingen/vuur'),
	('/tentoonstelling.php?item=2047','http://www.kunsthalkade.nl/nl/tentoonstellingen/now-japan'),
	('/agendaItem.php?item=3095','http://www.kunsthalkade.nl/nl/nu-en-verwacht/activiteiten/'),
	('/nieuws.php','http://www.kunsthalkade.nl/nl/over-kade/nieuws'),
	('/agendaItem.php?item=3138','http://www.kunsthalkade.nl/nl/nu-en-verwacht'),
	('/cafe.php?item=17','http://www.kunsthalkade.nl/nl/plan-je-bezoek/kadecafe'),
	('/over.php?item=22','http://www.kunsthalkade.nl/nl/over-kade'),
	('/tentoonstelling.php?item=2728&offset=0','http://www.kunsthalkade.nl/nl/tentoonstellingen/de-loop-der-dingen-over-oorzaak-gevolg'),
	('/educatie.php?item=2125','http://www.kunsthalkade.nl/nl/nu-en-verwacht/voor-kinderen'),
	('/nieuws.php?item=3140','http://www.kunsthalkade.nl/nl/over-kade/nieuws'),
	('/cafe.php?item=687','http://www.kunsthalkade.nl/nl/plan-je-bezoek/kadecafe'),
	('/tentoonstelling.php?item=2691','http://www.kunsthalkade.nl/nl/tentoonstellingen/expeditie-landart'),
	('/nieuws.php?item=3166','http://www.kunsthalkade.nl/nl/tentoonstellingen/de-kleuren-van-de-stijl')
]

def has_args(url):
	url_split = url.split("?")
	if len(url_split) > 1:
		return True

	return False

def extract_args(url):
	args = ""

	url_split = url.split("?")
	if len(url_split) > 1:
		return url_split[0], url_split[1]

	return url, args

def generate_args_dict(all_redirects):
	roots = {}
	for redirect in all_redirects:
		if has_args(redirect[0]):
			redirect_root, redirect_args = extract_args(redirect[0])
			if redirect_root not in roots:
				roots['%s'%(redirect_root)] = [(redirect_args, redirect[1])]
			else:
				roots['%s'%(redirect_root)].append((redirect_args, redirect[1]))

	return roots

def generate_args_part(roots):
	args_part = ""
	for key, value in roots.iteritems():
		all_args = ""

		for arg in value:
			arg_template = TEMPLATEINNER %(arg[0], arg[1])
			all_args += arg_template

		args_template = TEMPLATEARGS % (key, all_args)
		args_part += args_template

	return args_part


def generate_noargs_part(all_redirects):
	noargs_part = ""
	for redirect in all_redirects:
		if not has_args(redirect[0]):
			redirect_template = TEMPLATE %(redirect[0], redirect[1])
			noargs_part += redirect_template
	return noargs_part



def generate_final_file(roots, all_redirects):
	args_part = generate_args_part(roots)
	noargs_part = generate_noargs_part(all_redirects)

	final_file = args_part + noargs_part
	print final_file


redirects_sorted = sorted(redirects, key=lambda x: len(x[0].split('/')), reverse=True)
redirect_roots = generate_args_dict(redirects_sorted)
generate_final_file(redirect_roots, redirects_sorted)





