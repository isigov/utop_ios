#!/bin/bash

IPODNAME=ipod

LOCALDIR='/Users/illyasigov/Desktop/apple_ids'
REMOTEDIR='/private/var/mobile/Library'
APPLE_ID=$1

ssh ${IPODNAME} "rm -r ${REMOTEDIR}/com.apple.itunesstored"
ssh ${IPODNAME} "rm -r ${REMOTEDIR}/ConfigurationProfiles"
ssh ${IPODNAME} "rm -r ${REMOTEDIR}/Cookies"
ssh ${IPODNAME} "rm -r ${REMOTEDIR}/Passes"
ssh ${IPODNAME} "rm -r ${REMOTEDIR}/Preferences"
ssh ${IPODNAME} "rm -r ${REMOTEDIR}/TCC"

scp -r -P 2222 ${LOCALDIR}/${APPLE_ID}/'com.apple.itunesstored' ${IPODNAME}:${REMOTEDIR}/
scp -r -P 2222 ${LOCALDIR}/${APPLE_ID}/'ConfigurationProfiles' ${IPODNAME}:${REMOTEDIR}/
scp -r -P 2222 ${LOCALDIR}/${APPLE_ID}/'Cookies' ${IPODNAME}:${REMOTEDIR}/
scp -r -P 2222 ${LOCALDIR}/${APPLE_ID}/'Passes' ${IPODNAME}:${REMOTEDIR}/
scp -r -P 2222 ${LOCALDIR}/${APPLE_ID}/'Preferences' ${IPODNAME}:${REMOTEDIR}/
scp -r -P 2222 ${LOCALDIR}/${APPLE_ID}/'TCC' ${IPODNAME}:${REMOTEDIR}/

ssh ${IPODNAME} "chmod -R 777 ${REMOTEDIR}"

ssh ${IPODNAME} "reboot"
