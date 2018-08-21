/*
 * nf_skelton.c -- A POC program for DSR uplad accelerator.
 * 
 * Copyright (C) 2007  Masanori ITOH
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *	
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 * AUTHOR:
 *   Masanori ITOH  <masanori.itoh@gmail.com>
 *
 * $Id$
 */
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h> /* for dump_stack() */
#include <linux/types.h>

#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/skbuff.h>
#include <linux/ip.h>
#include <net/ip.h>
#include <linux/tcp.h>
#include <net/netns/generic.h>		/* net_generic() */

MODULE_AUTHOR("Masanori ITOH");
MODULE_DESCRIPTION("A simple module for network trouble shooting.");
MODULE_LICENSE("GPL");
MODULE_VERSION("1.0");


static int hook = NF_INET_PRE_ROUTING;
module_param(hook, int, 0644);
MODULE_PARM_DESC(hooks, "hook, netfilter hook points");

static int verbose = 2;
module_param(verbose, int, 0644);
MODULE_PARM_DESC(verbose, "verbose mode");

static unsigned int nf_skelton_net_id __read_mostly;

static unsigned int nf_skelton_hook(void *priv,
				    struct sk_buff *skb,
				    const struct nf_hook_state *state)
{
	if (verbose >= 2) {
		printk("%s: called: %p %p %p\n",
		       __FUNCTION__,
		       priv, skb, state);
	}
	return NF_ACCEPT;
}

static struct nf_hook_ops nf_skelton_hook_ops = {
	.hook     = nf_skelton_hook,
	.pf       = NFPROTO_IPV4,
	.hooknum  = 0,
	.priority = 100,
};

static int __net_init __nf_skelton_init(struct net *);
static void __net_exit __nf_skelton_exit(struct net *);

static int __net_init __nf_skelton_init(struct net *net)
{
	int ret;
	void *ptr;

	printk("%s: called: \n", __FUNCTION__);
	
	ptr = net_generic(net, nf_skelton_net_id);
	printk("%s: nf_skelton_id=%d ptr=%p \n", __FUNCTION__,
	       nf_skelton_net_id, ptr);
	/* FIXME: failure case ? */

	nf_skelton_hook_ops.hooknum = hook;
	ret = nf_register_net_hook(net, &nf_skelton_hook_ops);
	if (ret < 0) {
		return -ENOMEM;
	}
	return 0;
}
static void __net_exit __nf_skelton_exit(struct net *net)
{
	printk("%s: called: \n", __FUNCTION__);
	nf_unregister_net_hook(net, &nf_skelton_hook_ops);
        return;
}

static struct pernet_operations nf_skelton_ops = {
	.init = __nf_skelton_init,
	.exit = __nf_skelton_exit,
	.id   = &nf_skelton_net_id,
	.size = 0,
};

static void __net_exit nf_skelton_dev_cleanup(struct net *net)
{
	printk("%s: called\n", __FUNCTION__);
	return;
}

static struct pernet_operations nf_skelton_dev_ops = {
	.exit = nf_skelton_dev_cleanup,
};


static int __init nf_skelton_init(void)
{
	int ret;

	printk("%s: called. hook=%d verbose=%d\n", __FUNCTION__,
	       hook, verbose);

	ret = register_pernet_subsys(&nf_skelton_ops);
	if (ret < 0) {
		printk("%s: failed to register nf_skelton_ops\n",
		       __FUNCTION__);
		goto bailout_subsys;

	}
	ret = register_pernet_device(&nf_skelton_dev_ops);
	if (ret < 0) {
		printk("%s: failed to register nf_skelton_dev_ops\n",
		       __FUNCTION__);
		goto bailout_dev;
	}
	
	return 0;

bailout_dev:
	unregister_pernet_subsys(&nf_skelton_ops);

bailout_subsys:

	return -ENOMEM;
}

static void __exit nf_skelton_exit(void)
{
	printk("%s: called\n", __FUNCTION__);

	unregister_pernet_device(&nf_skelton_dev_ops);
	unregister_pernet_subsys(&nf_skelton_ops);

	return;
}

module_init(nf_skelton_init);
module_exit(nf_skelton_exit);

