#ifndef PARASETTINGS_H
#define PARASETTINGS_H

#include <QDialog>

namespace Ui {
class Parasettings;
}

class Parasettings : public QDialog
{
    Q_OBJECT

public:
    explicit Parasettings(QWidget *parent = 0);
    ~Parasettings();

private:
    Ui::Parasettings *ui;
};

#endif // PARASETTINGS_H
