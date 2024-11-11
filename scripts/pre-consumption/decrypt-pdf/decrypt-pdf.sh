#!/usr/bin/env bash

# paperless-ngx pre-consumption script
# https://docs.paperless-ngx.com/advanced_usage/#pre-consume-script
#
# uses qpdf to test consumed pdf for encryption and try a list of pre-supplied passwords
# if one matches, attempts to remove encryption from file
#
# the user can supply the lists of passwords via *.pwd.txt files
# the file 'personal.pwd.txt' is reserved for the user's true passwords and guarded
# via .gitignore against unintentional disclosure
#

# Environment Variable 		Description
# DOCUMENT_SOURCE_PATH 		Original path of the consumed document
# DOCUMENT_WORKING_PATH 	Path to a copy of the original that consumption will work on
# TASK_ID 					UUID of the task used to process the new document (if any)

SCRIPT_PATH=$(readlink -f "$0")
readonly SCRIPT_PATH
SCRIPT_DIR=$(dirname "${SCRIPT_PATH}")
readonly SCRIPT_DIR
SCRIPT_NAME=$(basename "${SCRIPT_PATH}")
readonly SCRIPT_NAME
CONSUMABLE=$(basename "${DOCUMENT_WORKING_PATH}")
readonly CONSUMABLE
FILE_TYPE=$(file --mime-type --brief --no-pad "${DOCUMENT_WORKING_PATH}")
readonly FILE_TYPE


printf -- '--- %(%F %H:%M:%S)T | %s -------------------------------------\n' -1 "${SCRIPT_NAME}"

if [[ "${FILE_TYPE,,}" != 'application/pdf' ]]; then
	printf '%s is not recognized as PDF file, nothing to do\n' "${CONSUMABLE}"

elif qpdf --is-encrypted "${DOCUMENT_WORKING_PATH}";  then

	# shellcheck disable=SC2046
	PWD_CORPUS=$(cat $(find "${SCRIPT_DIR}" -type f -iname '*.pwd.txt') | sort -u)
	readonly PWD_CORPUS
	PWD_COUNT=$(printf '%s' "${PWD_CORPUS}" | wc -l | cut -f 1 -d ' ')
	readonly PWD_COUNT
	printf 'password corpus with %u entries assembled\n' "${PWD_COUNT}"
	
	printf '%s is encrypted, trying to decrypt... ' "${CONSUMABLE}"
    decrypted=0

    while IFS= read -r pwd_line || [[ -n "${pwd_line}" ]]; do
    
        qpdf --requires-password --password="${pwd_line}" "${DOCUMENT_WORKING_PATH}"
        
        # exit codes: see https://qpdf.readthedocs.io/en/stable/cli.html#option-requires-password
        case $? in
            3)  
                qpdf --decrypt --password="${pwd_line}" "${DOCUMENT_WORKING_PATH}" --replace-input
                printf 'decrypted\n'
                decrypted=1
                
                printf 'password reminder:\n'
                case ${#pwd_line} in
                    1-2)
                        printf 'less than 3 characters long\n'
                        ;;
                        
                    3-5)
                        printf 'starts with %s and ends with %s\n' "${pwd_line: 0: 1}" "${pwd_line: -1}"
                        ;;
                        
                    *)
                        printf 'has %u characters, starts with %s and ends with %s\n' "${#pwd_line}" "${pwd_line: 0: 1}" "${pwd_line: -1}"
                        ;;
                esac
                
                break
                ;;
            
            *)
                continue
                ;;
        esac
    done < <(printf '%s' "${PWD_CORPUS}")
    
    if (( decrypted != 1 )); then
        printf 'failed\n'
        printf 'no password entry matches\n'
    fi

else
    printf '%s is unencrypted, nothing to do\n' "${CONSUMABLE}"
fi

printf -- '--- %(%F %H:%M:%S)T -------------------------------------\n' -1
