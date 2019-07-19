#include "encrypt.h"
#include "ui_encrypt.h"

encrypt::encrypt(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::encrypt)
{
    ui->setupUi(this);
}

encrypt::~encrypt()
{
    delete ui;
}
