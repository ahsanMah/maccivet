#include "maccivet.h"
#include "ui_maccivet.h"

maccivet::maccivet(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::maccivet)
{
    ui->setupUi(this);

    this->setCentralWidget(ui->tabWidget);
}

maccivet::~maccivet()
{
    delete ui;
}
