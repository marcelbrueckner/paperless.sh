#!/usr/bin/env bash

# paperless-ngx pre-consumption script
# https://docs.paperless-ngx.com/advanced_usage/#pre-consume-script
#
# uses qpdf to test consumed pdf for encryption and try a list of pre-supplied passwords
# if one matches, attempts to remove encryption from file
#

#Environment Variable 	Description
# DOCUMENT_SOURCE_PATH 	Original path of the consumed document
# DOCUMENT_WORKING_PATH 	Path to a copy of the original that consumption will work on
# TASK_ID 	UUID of the task used to process the new document (if any)
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
SCRIPT_NAME=$(basename "$SCRIPT_PATH")
CONSUMABLE=$(basename "$DOCUMENT_WORKING_PATH")

printf -- '--- %(%F %H:%M:%S)T | %s -------------------------------------\n' -1 ${SCRIPT_NAME}

PWDCOUNT=$(wc -l "$SCRIPT_DIR/passwords.txt" | cut -f 1 -d ' ')
printf 'passwords.txt has %u entries.\n' ${PWDCOUNT}

if qpdf --is-encrypted "$DOCUMENT_WORKING_PATH"; then
    DECODED=0
    printf '%s is encrypted, trying to decrypt... ' ${CONSUMABLE}
    
    IFS=''
    while read -r pwd_line; do
        qpdf --requires-password --password="$pwd_line" "$DOCUMENT_WORKING_PATH"
        
        case $? in
            3)
                qpdf --decrypt --password="$pwd_line" "$DOCUMENT_WORKING_PATH" --replace-input
                printf 'decrypted\n'
                DECODED=1
                if [ ${#pwd_line} -ge 5 ] ; then
                    printf 'password reminder: password has %u characters, starts with %s and ends with %s\n' \
                        $(echo -n $pwd_line | wc -m ) \
                        ${pwd_line: 0: 1} \
                        ${pwd_line: -1}
                fi
                
                break
                ;;
            
            *)
                continue
                ;;
        esac
    done < "$SCRIPT_DIR/passwords.txt"
    
    if [[ "$DECODED" -ne "1" ]]; then
        printf '\ndecryption attempt failed, no password entry matches\n'
    fi

else
    printf '%s is unencrypted, nothing to do\n' ${CONSUMABLE}
fi

printf -- '--- %(%F %H:%M:%S)T -------------------------------------\n' -1
