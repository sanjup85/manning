import smtplib
import random
import unicodecsv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# control parameters for the program
log_debug_messages = False
from_email_id = 'xxxx@xxxx.com'
login_password = 'xxxxxxxxxxxx'
smtp_host_name = 'smtp.gmail.com'
smtp_port_value = 465
input_file_name = 'inputs/exam.csv'


def get_input_csv_records(input_file_name):
    dict_reader = unicodecsv.DictReader(open(input_file_name, 'rb'), encoding='latin1')
    input_file_contents = list(dict_reader)
    if log_debug_messages:
        for input_record in input_file_contents:
            print(f'processing: {input_record}')
    return input_file_contents


def send_communication(list_records):
    server = smtplib.SMTP_SSL(smtp_host_name, smtp_port_value)
    server.login(from_email_id, login_password)
    randomly_selected_message = 'You’ve been randomly chosen to present a summary of the book in the next class. Looking forward to it!'
    selected_record = random.choice(list_records)
    for record in list_records:
        to_email_id = record['Email']
        first_name = record['First Name']
        last_name = record['Last Name']
        # presume valid email is present in the CSV - no validation logic added
        multipart_message = MIMEMultipart()
        multipart_message['From'] = from_email_id
        multipart_message['To'] = to_email_id
        multipart_message['Subject'] = f'Test Result - {last_name}, {first_name}'
        if selected_record == record:
            randomly_selected = randomly_selected_message
        else:
            randomly_selected = ''
        email_body = f'Dear {first_name}, Your score for the book assignment is broken down below by question number.\n' \
                     f'\n' \
                     f'1. {record["Problem 1 score"]}%: {record["Problem 1 comments"]}\n' \
                     f'2. {record["Problem 2 score"]}%: {record["Problem 2 comments"]}\n' \
                     f'3. {record["Problem 3 score"]}%: {record["Problem 3 comments"]}\n' \
                     f'\n' \
                     f'{randomly_selected}'

        multipart_message.attach(MIMEText(email_body, 'plain'))
        text = multipart_message.as_string()
        print(text)
        server.sendmail(
            from_addr=from_email_id,
            to_addrs=to_email_id,
            msg=text)
    server.quit()


def automate_email():
    # read the input CSV file and save the input records
    list_records = get_input_csv_records(input_file_name)

    # save the input records and mail the results
    send_communication(list_records)


# execute the automate email method
automate_email()
