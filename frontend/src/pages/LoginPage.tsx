import { useState } from 'react'
import type { FormEvent } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router'
import { RiBankLine, RiFlashlightLine, RiLock2Line, RiPulseLine, RiSparkling2Line } from '@remixicon/react'
import LoginForm from '@/components/auth/LoginForm'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useAuth } from '@/context/AuthContext'
import { paths } from '@/routes/paths'

function LoginPage() {
  const { login, token } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [error, setError] = useState('')
  const registered = Boolean((location.state as { registered?: boolean } | null)?.registered)
  if (token) return <Navigate to={paths.account} replace />

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    const form = new FormData(event.currentTarget)
    try {
      await login(String(form.get('email')), String(form.get('password')))
      navigate(paths.account)
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Unable to log in.')
    }
  }

  return (
    <main className="grid min-h-screen lg:grid-cols-[1.15fr_.85fr]">
      <section className="relative hidden overflow-hidden bg-[#123f35] p-10 text-white lg:flex lg:flex-col lg:justify-between xl:p-12">
        <div className="relative z-10 flex items-center gap-3"><span className="brand-mark"><RiBankLine aria-hidden="true" /></span><span className="font-heading text-2xl font-bold">Dinero</span></div>
        <div className="relative z-10 mt-10 max-w-2xl">
          <p className="mb-4 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/10 px-4 py-2 text-sm"><RiFlashlightLine className="size-4" /> Your Financial Partner for Life</p>
          <h1 className="max-w-xl font-heading text-5xl font-semibold leading-[1.03] xl:text-6xl">Get Your Money Up, Not Your Funny Up</h1>
<p className="mt-5 text-lg leading-relaxed text-emerald-50/75">
  Track your income, expenses, and account activity with Dinero:
  <br />
  a clear and secure banking experience that is built around you
</p>
</div>
        <div className="relative z-10 my-8 overflow-hidden rounded-[2rem] border border-white/10 shadow-2xl">
          <img alt="A cheerful coin relaxing while its savings grow" className="h-64 w-full object-cover xl:h-72" src="/assets/dinero-hero.png" />
          <div className="absolute inset-x-0 bottom-0 flex items-center gap-2 bg-gradient-to-t from-[#0d332a] to-transparent px-6 pb-5 pt-16 text-sm font-medium"><RiSparkling2Line className="size-4 text-amber-300" /> Let your balance do the heavy lifting</div>
        </div>
        <div className="relative z-10 grid grid-cols-3 gap-4 text-sm text-emerald-50/70">
          <span className="flex items-center gap-2"><RiLock2Line /> JWT protected</span><span className="flex items-center gap-2"><RiPulseLine /> Live activity</span><span className="flex items-center gap-2"><RiBankLine /> MongoDB backed</span>
        </div>
      </section>
      <section className="login-form-panel flex items-center justify-center p-6 sm:p-10">
        <div className="relative z-10 w-full max-w-md">
          <div className="mb-8 flex items-center gap-3 lg:hidden"><span className="brand-mark"><RiBankLine aria-hidden="true" /></span><span className="font-heading text-xl font-bold">Dinero</span></div>
          {registered && <Alert className="mb-4 border-emerald-200 bg-emerald-50"><AlertDescription>Your profile is ready. Sign in to access your accounts.</AlertDescription></Alert>}
          {error && <Alert className="mb-4" variant="destructive"><AlertDescription>{error}</AlertDescription></Alert>}
          <LoginForm onSubmit={handleSubmit} />
          {/* <p className="mt-5 text-center text-xs text-muted-foreground">Your session token is kept only for this browser tab.</p> */}
        </div>
      </section>
    </main>
  )
}

export default LoginPage
