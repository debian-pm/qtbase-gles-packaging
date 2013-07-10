#! /bin/sh

PRIVATE_HEADERS=qtbase5-private-dev/usr/include

error() {
	echo $@
	exit 1
}

debug() {
	[ -n "${DEBUG}" ] && echo $@
}

if [ ! -e "${PRIVATE_HEADERS}" ] 
then
	error "Private headers not found"
fi

grep -rh class ${PRIVATE_HEADERS} |
	grep EXPORT | 
	while read class export classname rest 
	do
		echo ${#classname}${classname} 
	done | 
	while read privateclass 
	do
		debug marking ${privateclass} as private
		sed -i "s/\(.*${privateclass}[^ ]* *[^ ]*\)$/\1 1/" *.symbols 
	done 

