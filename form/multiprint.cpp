#include "multiprint.h"
#include "ui_multiprint.h"

MultiPrint::MultiPrint(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::MultiPrint)
{
    ui->setupUi(this);
}

MultiPrint::~MultiPrint()
{
    delete ui;
}
