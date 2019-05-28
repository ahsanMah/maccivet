#include "maccivet.h"
#include "ui_maccivet.h"

maccivet::maccivet(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::maccivet)
{
    ui->setupUi(this);
}

maccivet::~maccivet()
{
    delete ui;
}
