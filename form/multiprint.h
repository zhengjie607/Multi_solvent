#ifndef MULTIPRINT_H
#define MULTIPRINT_H

#include <QWidget>

namespace Ui {
class MultiPrint;
}

class MultiPrint : public QWidget
{
    Q_OBJECT

public:
    explicit MultiPrint(QWidget *parent = 0);
    ~MultiPrint();

private:
    Ui::MultiPrint *ui;
};

#endif // MULTIPRINT_H
