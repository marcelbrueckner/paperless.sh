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

echo "--- $(TZ=$PAPERLESS_TIME_ZONE date '+%F %H:%M:%S') | $(basename "$SCRIPT_PATH") -------------------------------------"

PWDCOUNT=$(wc -l "$SCRIPT_DIR/passwords.txt" | cut -f 1 -d ' ')
echo "passwords.txt has $PWDCOUNT entries."

if qpdf --is-encrypted "$DOCUMENT_WORKING_PATH"; then
    echo "$(basename "$DOCUMENT_WORKING_PATH") is encrypted, trying to decrypt..."
    DECODED=0
    
    IFS=''
    while read -r pwd_line; do
        qpdf --requires-password --password="$pwd_line" "$DOCUMENT_WORKING_PATH"
        
        case $? in
            3)
                qpdf --decrypt --password="$pwd_line" "$DOCUMENT_WORKING_PATH" --replace-input
                echo "decrypted"
                DECODED=1
                if [ ${#pwd_line} -ge 5 ] ; then
                    echo "password reminder: password has $(echo -n $pwd_line | wc -m ) characters, starts with ${pwd_line: 0: 1} and ends with ${pwd_line: -1}"
                fi
                
                break
                ;;
            
            *)
                continue
                ;;
        esac
    done < "$SCRIPT_DIR/passwords.txt"
    
    if [[ "$DECODED" -ne "1" ]]; then
        echo "decryption attempt failed, no password entry matches"
    fi

else
    echo "$(basename "$DOCUMENT_WORKING_PATH") is unencrypted, nothing to do"
fi

echo "--- $(TZ=$PAPERLESS_TIME_ZONE date '+%F %H:%M:%S') -------------------------------------"
