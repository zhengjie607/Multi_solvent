#include "parasettings.h"
#include "ui_parasettings.h"

Parasettings::Parasettings(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Parasettings)
{
    ui->setupUi(this);
}

Parasettings::~Parasettings()
{
    delete ui;
}
