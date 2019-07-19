#ifndef ENCRYPT_H
#define ENCRYPT_H

#include <QDialog>

namespace Ui {
class encrypt;
}

class encrypt : public QDialog
{
    Q_OBJECT

public:
    explicit encrypt(QWidget *parent = 0);
    ~encrypt();

private:
    Ui::encrypt *ui;
};

#endif // ENCRYPT_H
