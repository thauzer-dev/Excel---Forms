            self.assertIsNone(MINIMOSE([1], ['A'], 'B'))
            self.assertEqual(CONT_VALORES([None, '', 0, False, 'A']), 3)

        def test_calendario(self):
            self.assertEqual(FIMMES('10/02/2024'), date(2024, 2, 29))
            self.assertEqual(FIMMES_DESLOCADO('2024-01-15', 2), date(2024, 3, 31))
            self.assertEqual(DATAM('2024-01-31', 1), date(2024, 2, 29))
            self.assertEqual((ANO('15/06/2024'), MES('15/06/2024'), DIA('15/06/2024')), (2024, 6, 15))
            self.assertEqual(DIAS('2024-01-02T01:00:00', '2024-01-01T23:00:00'), 1)
            for entrada in (None, 45000, '31/02/2024', pd.NaT):
                with self.assertRaises(ValueError):
                    ANO(entrada)

        def test_datadif(self):
            self.assertEqual(DATADIF('2020-01-01', '2024-06-15', 'M'), 53)
            self.assertEqual(DATADIF('2020-02-29', '2021-02-28', 'D'), 365)
            self.assertEqual(DATADIF('2020-02-29', '2021-02-28', 'Y'), 0)
            self.assertEqual(DATADIF('2020-02-29', '2021-02-28', 'YD'), 0)
            self.assertEqual(DATADIF('2023-11-20', '2024-02-10', 'YD'), 82)
            self.assertEqual(DATADIF('2024-01-31', '2024-02-29', 'M'), 0)
            self.assertEqual(DATADIF('2024-01-31', '2024-02-29', 'MD'), 0)
            self.assertEqual(DATADIF('2020-01-01', '2024-06-15', 'YM'), 5)
            with self.assertRaises(ValueError):
                DATADIF('2024-02-01', '2024-01-01')

        def test_dias_uteis(self):
            self.assertEqual(DIATRABALHOTOTAL('2024-01-01', '2024-01-31'), 23)
            self.assertEqual(DIATRABALHOTOTAL('2024-01-31', '2024-01-01', ['2024-01-01']), -22)
            self.assertEqual(DIATRABALHOTOTAL('2024-01-06', '2024-01-06'), 0)
            self.assertEqual(DIATRABALHOTOTAL('2024-01-01', '2024-01-01'), 1)
            self.assertEqual(DIATRABALHO('2024-01-06', 1), date(2024, 1, 8))
            self.assertEqual(DIATRABALHO('2024-01-07', -1), date(2024, 1, 5))
            self.assertEqual(DIATRABALHO('2024-01-06', 0), date(2024, 1, 6))
            self.assertEqual(DIATRABALHOTOTAL('2024-01-01', '2024-01-07', semana_util='1111110'), 6)

        def test_intervalo_mtd(self):
            self.assertEqual(INICIO_MES_ATE_HOJE_MENOS1('2024-03-01', primeiro_dia='mes_anterior'),
                             (date(2024, 2, 1), date(2024, 2, 29)))
            ini, fim = INICIO_MES_ATE_HOJE_MENOS1('2024-03-01')
            self.assertGreater(ini, fim)

        def test_indicadores(self):
            self.assertEqual(MARGEM(100, 60), .4)
            self.assertEqual(CRESCIMENTO(-80, -100), .2)
            self.assertEqual(TICKET_MEDIO(5000, 25), 200)
            self.assertEqual(PARTICIPACAO(30, 100), .3)
            self.assertTrue(np.isnan(DIVIDIR(1, 0)))
            self.assertTrue(np.isnan(DIVIDIR(None, 10)))
            self.assertTrue(np.isnan(DIVIDIR(1, np.inf)))
            np.testing.assert_allclose(MARGEM([100, 0], [60, 20]), [.4, np.nan], equal_nan=True)
            a = pd.Series([100, 200], index=['a', 'b'])
            b = pd.Series([60, 100], index=['b', 'a'])
            pd.testing.assert_series_equal(MARGEM(a, b), pd.Series([.4, .5], index=['a', 'b']))
            with self.assertRaises(ValueError):
                DIVIDIR([1, 2], [1])
            np.testing.assert_allclose(SHARE([100, 200, 200]), [.2, .4, .4])
            self.assertTrue(SHARE([0, 0]).isna().all())

        def test_variacao_sem_preenchimento(self):
            s = pd.Series([100, None, 120, 0, 10], index=list('abcde'))
            r = VARIACAO_M1(s)
            self.assertTrue(r.iloc[:3].isna().all())
            self.assertEqual(r.iloc[3], -1)
            self.assertTrue(np.isnan(r.iloc[4]))
            self.assertEqual(r.index.tolist(), s.index.tolist())
            self.assertEqual(VARIACAO_Y1(range(1, 25)).iloc[12], 12)

        def test_merge_validacao_e_imutabilidade(self):
            a, b = pd.DataFrame({'id': [1, 2]}), pd.DataFrame({'id': [1, 1], 'v': [2, 3]})
            copia = a.copy(deep=True)
            with self.assertRaises(pd.errors.MergeError):
                MERGE(a, b, 'id', validar='many_to_one')
            MERGE(a, b, 'id')
            pd.testing.assert_frame_equal(a, copia)

        def test_complementos(self):
            self.assertEqual(SOMARPRODUTO([10, 20], [2, 3]), 80)
            self.assertEqual(VALOR('R$ 1.234,56'), 1234.56)
            self.assertEqual(VALOR('12,5%'), .125)
            self.assertEqual(VALOR('1,234.56', decimal='.', milhar=','), 1234.56)
            with self.assertRaises(ValueError):
                VALOR('1.2.3')
            self.assertEqual(ARRED(2.675, 2), 2.68)
            self.assertEqual(ARRED(-2.5), -3)
            self.assertEqual(ARRED(125, -1), 130)
            self.assertEqual(ARRUMAR('  Olá \t mundo  '), 'Olá mundo')
            self.assertEqual(ESQUERDA('abcd', 2), 'ab')
            self.assertEqual(DIREITA('abcd', 0), '')
            self.assertEqual(EXT_TEXTO('abcd', 2, 2), 'bc')
            self.assertEqual(SE(pd.NA, 'sim', 'não'), 'não')
            self.assertEqual(SEERRO(lambda: 1 / 0, 9), 9)
            self.assertEqual(SEERRO(np.nan, 9), 9)
            self.assertEqual(UNICOS(['a', 'a', 'b']).tolist(), ['a', 'b'])
            df = pd.DataFrame({'x': [1, 2]}, index=[20, 10])
            self.assertEqual(FILTRO(df, [False, True]).index.tolist(), [10])
            self.assertEqual(FILTRO(df, [False, False], 'vazio'), 'vazio')
            with self.assertRaises(TypeError):
                FILTRO(df, ['sim', 'não'])

    resultado = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Regressao))
    return 0 if resultado.wasSuccessful() else 1


def _main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument('--demo', action='store_true', help='Executa exemplos fictícios.')
    grupo.add_argument('--test', action='store_true', help='Executa testes de regressão.')
    grupo.add_argument('--listar', action='store_true', help='Lista as funções disponíveis.')
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()
    if args.test:
        return _testes()
    if args.demo:
        _demo()
    elif args.listar:
        for nome in __all__:
            print(f'{nome}: {globals()[nome].__doc__.strip().splitlines()[0]}')
    else:
        parser.print_help()
    return 0


if __name__ == '__main__':
    raise SystemExit(_main())
