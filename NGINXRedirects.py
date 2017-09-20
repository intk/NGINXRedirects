# -*- coding: utf-8 -*-

TEMPLATE = 'location ~ ^%s {\n\trewrite ^ %s? permanent;\n}\n'
TEMPLATE_ARGS =  'location ~ ^%s {%s}\n'
TEMPLATE_INNER = "\n\tif ($args ~ %s) {\n\t\trewrite ^ %s? permanent;\n\t}\n"


redirects = [
	('/oldurl.php','http://www.example.com/new/path'),
	('/oldurl.php?item=51','http://www.example.com/new/path/item'),
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
			arg_template = TEMPLATE_INNER %(arg[0], arg[1])
			all_args += arg_template

		args_template = TEMPLATE_ARGS % (key, all_args)
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


if __name__ == "__main__":
	redirects_sorted = sorted(redirects, key=lambda x: len(x[0].split('/')), reverse=True)
	redirect_roots = generate_args_dict(redirects_sorted)
	generate_final_file(redirect_roots, redirects_sorted)





