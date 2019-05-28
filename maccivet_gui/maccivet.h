#ifndef MACCIVET_H
#define MACCIVET_H

#include <QMainWindow>

namespace Ui {
class maccivet;
}

class maccivet : public QMainWindow
{
    Q_OBJECT

public:
    explicit maccivet(QWidget *parent = nullptr);
    ~maccivet();

private:
    Ui::maccivet *ui;
};

#endif // MACCIVET_H
